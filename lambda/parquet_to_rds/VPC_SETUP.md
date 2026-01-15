# VPC Configuration for Lambda to Access RDS

If your RDS PostgreSQL database is in a VPC (which is the default), your Lambda function must also be in the same VPC to access it.

## Important Notes

- **RDS Endpoint**: `database-1.c3ea24kmsrmf.ap-south-1.rds.amazonaws.com`
- If this RDS instance is in a VPC, Lambda must be configured to access that VPC

## Steps to Configure VPC Access

### 1. Identify RDS VPC Configuration

1. Go to AWS RDS Console
2. Select your database instance
3. Note the **VPC ID** and **Subnet Group**
4. Note the **Security Group** attached to RDS

### 2. Configure Lambda VPC Settings

#### Option A: Using SAM Template

Add VPC configuration to `template.yaml`:

```yaml
Resources:
  ParquetToRDSFunction:
    Type: AWS::Serverless::Function
    Properties:
      # ... existing properties ...
      VpcConfig:
        SecurityGroupIds:
          - sg-xxxxxxxxx  # Security group that allows outbound connections
        SubnetIds:
          - subnet-xxxxxxxxx  # Private subnet 1
          - subnet-yyyyyyyyy  # Private subnet 2 (for high availability)
```

#### Option B: Using AWS Console

1. Go to Lambda function → **Configuration** → **VPC**
2. Click **Edit**
3. Select:
   - **VPC**: Same VPC as RDS
   - **Subnets**: At least 2 subnets (for high availability)
   - **Security groups**: A security group that allows:
     - Outbound: All traffic (or at least to RDS port 5432)
4. Click **Save**

### 3. Update RDS Security Group

The RDS security group must allow inbound connections from Lambda's security group:

1. Go to RDS → Your database → **Connectivity & security**
2. Click on the **Security group**
3. Go to **Inbound rules** → **Edit inbound rules**
4. Add rule:
   - **Type**: PostgreSQL (port 5432)
   - **Source**: Select the Lambda security group
   - **Description**: Allow Lambda access
5. Click **Save rules**

### 4. Required IAM Permissions

The Lambda execution role needs VPC access permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:CreateNetworkInterface",
        "ec2:DescribeNetworkInterfaces",
        "ec2:DeleteNetworkInterface",
        "ec2:AssignPrivateIpAddresses",
        "ec2:UnassignPrivateIpAddresses"
      ],
      "Resource": "*"
    }
  ]
}
```

The SAM template should automatically add this via `AWSLambdaVPCAccessExecutionRole` policy.

## Important Considerations

### Cold Start Impact
- Lambda functions in VPC have longer cold starts (10+ seconds)
- Consider using provisioned concurrency for production workloads

### Timeout Settings
- VPC connections add latency
- Ensure timeout is sufficient (15 minutes recommended)

### Network Configuration
- Use **private subnets** for Lambda (not public subnets)
- Ensure subnets have internet access via NAT Gateway (if Lambda needs to access S3 or other AWS services)
- Or use VPC endpoints for S3 access

## Testing VPC Connectivity

After configuring VPC:

1. Test Lambda function with a small parquet file
2. Check CloudWatch Logs for connection errors
3. If connection fails, verify:
   - Lambda and RDS are in same VPC
   - Security group rules are correct
   - Subnets have proper routing

## Alternative: RDS Public Access (Not Recommended)

If RDS has public access enabled, Lambda doesn't need VPC configuration, but this is **not recommended** for production due to security concerns.







