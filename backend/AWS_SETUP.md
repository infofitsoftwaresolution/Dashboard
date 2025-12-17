# AWS RDS Security Group Setup Guide

## Quick Fix: Allow Your IP Address

To allow the migration script to connect to your RDS database, you need to add your IP address to the security group.

### Step-by-Step Instructions

1. **Go to AWS Console**
   - Navigate to: https://console.aws.amazon.com/rds/
   - Select your region (us-east-1)

2. **Find Your Database**
   - Click on "Databases" in the left menu
   - Find your database: `database-1` (or the one matching your hostname)
   - Click on the database name

3. **Access Security Groups**
   - Scroll down to "Connectivity & security" section
   - Find "VPC security groups"
   - Click on the security group link (e.g., `sg-xxxxx`)

4. **Edit Inbound Rules**
   - Click on the "Inbound rules" tab
   - Click "Edit inbound rules"
   - Click "Add rule"

5. **Add PostgreSQL Rule**
   - **Type**: PostgreSQL
   - **Protocol**: TCP
   - **Port**: 5432
   - **Source**: 
     - Option 1: "My IP" (if available) - automatically uses your current IP
     - Option 2: Custom - Enter your IP address (e.g., `123.45.67.89/32`)
   - **Description**: "Allow migration script"
   - Click "Save rules"

6. **Verify**
   - The rule should appear in your inbound rules list
   - Wait 1-2 minutes for changes to propagate

### Finding Your IP Address

**Windows:**
```powershell
# PowerShell
(Invoke-WebRequest -Uri "https://api.ipify.org").Content
```

**Or check online:**
- Visit: https://whatismyipaddress.com/
- Copy your IPv4 address

### Testing Connection

After adding your IP, test the connection:

```bash
cd backend
python -c "from sqlalchemy import create_engine; engine = create_engine('postgresql://username:password@database-1.cpueg8cau0g0.us-east-1.rds.amazonaws.com:5432/postgres'); conn = engine.connect(); print('✅ Connection successful!')"
```

Replace `username` and `password` with your actual credentials.

## Alternative: Use AWS VPN or Bastion Host

If you can't add your IP directly:

1. **AWS VPN**: Connect through AWS VPN
2. **Bastion Host**: Use an EC2 instance as a jump host
3. **AWS Systems Manager**: Use Session Manager for secure access

## Troubleshooting

### Still Can't Connect?

1. **Check Security Group Rules**
   - Verify the rule was saved
   - Check the IP address is correct (no typos)
   - Ensure port 5432 is open

2. **Check Network ACLs**
   - VPC Network ACLs might be blocking traffic
   - Check both inbound and outbound rules

3. **Check Database Status**
   - Ensure database is in "Available" state
   - Check if database is publicly accessible (if needed)

4. **Check Route Tables**
   - Verify routes allow traffic to RDS subnet

5. **Test from EC2**
   - Try connecting from an EC2 instance in the same VPC
   - This helps isolate if it's a network or security group issue

### Common Errors

**"Connection timed out"**
- Security group doesn't allow your IP
- Network ACL blocking traffic
- Database not publicly accessible

**"Password authentication failed"**
- Wrong username or password
- User doesn't exist
- User doesn't have proper permissions

**"Database does not exist"**
- Wrong database name
- Database hasn't been created yet

## After Security Group is Fixed

Once your IP is whitelisted, you can run the migration:

```bash
cd backend
python run_migration.py
```

Or provide credentials as arguments:

```bash
python run_migration.py --username YOUR_USER --password YOUR_PASS --database postgres
```

## Security Best Practices

⚠️ **Important Security Notes:**

1. **Remove IP After Migration**: Consider removing the IP rule after migration is complete
2. **Use Specific IPs**: Use `/32` CIDR for single IP addresses
3. **Time-Limited Rules**: Set expiration dates if possible
4. **Use IAM Authentication**: Consider using IAM database authentication for better security
5. **VPN Access**: For production, use VPN instead of direct IP access

## Need Help?

If you're still having issues:

1. Check AWS CloudWatch logs for database errors
2. Verify database endpoint is correct
3. Test connection from AWS CloudShell
4. Contact AWS Support if needed

---

**Once your security group is configured, the migration script will work!** 🚀

