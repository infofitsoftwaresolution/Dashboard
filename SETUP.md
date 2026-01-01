Perfect 👍
Below is a **fully beautified, human-friendly, and 100% copy-paste ready `SETUP.md`**.
Just **copy and paste as-is** — no edits needed.

---

```md
# 🛠️ Setup Guide – AWS Athena & S3 Data Pipeline Dashboard

This guide walks you through setting up **AWS S3**, **AWS Athena**, and running the **FastAPI + React analytics dashboard** end to end.

---

## 📋 Table of Contents

1. Prerequisites  
2. Project Structure  
3. AWS S3 Setup  
4. AWS Athena Setup  
5. SQL Queries Reference  
6. Application Setup  
7. API Endpoints  
8. Troubleshooting  

---

## ✅ Prerequisites

Make sure you have the following:

- Python **3.8+**
- Node.js **16+** and npm
- AWS Account with:
  - S3 access
  - Athena access
  - IAM user with required permissions

---

## 🏗️ Project Structure

```

Dashboard/
├── backend/
│   ├── api/                        # All API code organized here
│   │   ├── __init__.py
│   │   ├── models.py               # Pydantic models (Metric, TopUser, etc.)
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── dashboard.py        # Dashboard endpoints (/api/metrics, /api/top-users, etc.)
│   │       └── athena.py           # Athena endpoints (/api/athena/*)
│   ├── main.py                     # FastAPI app entry point
│   ├── athena_service.py           # Athena service layer
│   ├── requirements.txt
│   ├── env.example
│   └── venv/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── athena/
│   ├── create_table_ACTUAL.sql
│   ├── create_view.sql
│   ├── FIX_0_RESULTS.sql
│   ├── GET_ALL_DATA_ACTUAL.sql
│   ├── save_results_to_s3_ACTUAL.sql
│   └── VERIFY_ALL_FILES.sql
│
├── README.md
└── SETUP.md

```

---

## ☁️ AWS S3 Setup

### Step 1: Create S3 Bucket

1. Open AWS S3 Console
2. Click **Create bucket**
3. Configure:
   - Bucket name: `athena-data-bucket-data`
   - Region: `ap-south-1`
   - Block public access: Enabled
4. Create bucket

---

### Step 2: Folder Structure

Create this structure inside the bucket:

```

s3://athena-data-bucket-data/
├── audit-trail-data/
│   ├── raw/
│   └── processed/
└── athena-results/

```

---

### Step 3: Upload Parquet Files

Upload files to:

```

s3://athena-data-bucket-data/audit-trail-data/raw/

````

Upload methods:
- AWS Console (drag & drop)
- AWS CLI
- Python (boto3)

---

### Step 4: S3 Permissions

Attach this policy to your IAM user:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket",
        "s3:GetBucketLocation"
      ],
      "Resource": [
        "arn:aws:s3:::athena-data-bucket-data",
        "arn:aws:s3:::athena-data-bucket-data/*"
      ]
    }
  ]
}
````

---

## 🔍 AWS Athena Setup

### Step 1: IAM User Permissions

Attach this policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "athena:*",
        "glue:GetDatabase",
        "glue:GetTable",
        "glue:GetPartitions"
      ],
      "Resource": "*"
    }
  ]
}
```

Create **Access Key** and save:

* AWS_ACCESS_KEY_ID
* AWS_SECRET_ACCESS_KEY

---

### Step 2: Athena Workgroup

Set query result location:

```
s3://athena-data-bucket-data/athena-results/
```

---

### Step 3: Create Database

```sql
CREATE DATABASE IF NOT EXISTS audit_trail_db;
```

---

### Step 4: Create Table

Run `athena/create_table_ACTUAL.sql`

Update location if needed:

```sql
LOCATION 's3://athena-data-bucket-data/audit-trail-data/raw/'
```

---

### Step 5: Repair Table

```sql
MSCK REPAIR TABLE audit_trail_data;
```

---

### Step 6: Verify Data

```sql
SELECT COUNT(*) FROM audit_trail_data;
```

---

## 📄 SQL Queries Reference

All queries are located in the `athena/` folder:

* create_table_ACTUAL.sql
* create_view.sql
* FIX_0_RESULTS.sql
* GET_ALL_DATA_ACTUAL.sql
* save_results_to_s3_ACTUAL.sql
* VERIFY_ALL_FILES.sql

Run them directly in Athena Console.

---

## 🚀 Application Setup

### Step 1: Clone Repository

```bash
git clone https://github.com/infofitsoftwaresolution/Dashboard.git
cd Dashboard
```

---

### Step 2: Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy env.example .env
```

Linux / Mac:

```bash
source venv/bin/activate
cp env.example .env
```

Edit `.env`:

```env
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=ap-south-1
S3_BUCKET_NAME=athena-data-bucket-data
S3_PREFIX=audit-trail-data/raw/
S3_RESULTS_BUCKET=athena-data-bucket-data
S3_RESULTS_PREFIX=athena-results/
ATHENA_DATABASE_NAME=audit_trail_db
ATHENA_TABLE_NAME=audit_trail_data
ATHENA_WORKGROUP=primary
```

Start backend:

```bash
python main.py
```

---

### Step 3: Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

### Step 4: Access Dashboard

```
http://localhost:5173
```

---

## 🔌 API Documentation

### API Structure

All API code is organized in the `backend/api/` folder:

* **Models**: `api/models.py` - All Pydantic models for request/response validation
* **Dashboard Routes**: `api/routes/dashboard.py` - Dashboard metrics and reports endpoints
* **Athena Routes**: `api/routes/athena.py` - Athena-specific query endpoints
* **Main App**: `main.py` - FastAPI app setup and router registration

### API Endpoints

**Dashboard Endpoints** (`/api/*`):
* `GET /api/metrics` - Dashboard metrics
* `GET /api/top-users` - Top users data
* `GET /api/active-users` - Active users count
* `GET /api/staff-speaking` - Staff speaking statistics
* `GET /api/times` - Time-based analytics
* `GET /api/consents` - Consent data
* `GET /api/filter-options` - Available filter options
* `GET /api/audit-summary` - Audit trail summary
* `GET /api/patient-access` - Patient access logs
* `GET /api/signed-notes` - Signed notes
* `GET /api/unsigned-notes` - Unsigned notes
* `GET /api/practitioner-service-usage` - Practitioner usage stats
* `GET /api/sync-issues` - Sync issues report

**Athena Endpoints** (`/api/athena/*`):
* `GET /api/athena/data` - Query Athena data with filters
* `GET /api/athena/summary` - Summary statistics
* `GET /api/athena/dashboard` - Dashboard data view
* `GET /api/athena/all-data` - Fetch ALL data (no limit)
* `GET /api/athena/verify-files` - Verify S3 Parquet files
* `GET /api/athena/repair-table` - Repair Athena table metadata
* `POST /api/athena/query` - Execute custom Athena query

### Interactive API Documentation

* **Swagger UI**: `http://localhost:8000/docs`
* **ReDoc**: `http://localhost:8000/redoc`

---

## 🐞 Troubleshooting

### No Data in Athena

* Run `MSCK REPAIR TABLE audit_trail_data`
* Verify S3 path matches table LOCATION
* Check IAM permissions

### Backend Issues

* Python 3.8+
* `.env` configured correctly
* AWS credentials valid
* Virtual environment activated
* All dependencies installed (`pip install -r requirements.txt`)
* API routes properly imported (check `main.py` imports)

### Frontend Issues

* Node 16+
* Backend running on port 8000
* No CORS errors

---

## ✅ Final Checklist

* S3 bucket created
* Parquet files uploaded
* Athena database & table ready
* Backend running
* Frontend running
* Dashboard accessible

🎉 **Setup complete!**

