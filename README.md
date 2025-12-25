
## ✨ What This App Can Do

* 📊 **Real‑time Dashboard Metrics**
  See key numbers at a glance with trend indicators

* 📈 **Interactive Charts**
  Line, Bar, Pie, and Area charts powered by Recharts

* 🔍 **Smart Filters**

  * Date & month range filters
  * Practitioner, Program, and Location filters
  * All updates happen instantly

* ☁️ **AWS Athena Integration**

  * Direct querying of S3 Parquet files
  * No local database required
  * Real-time data from S3

* 📑 **Multiple Reports**

  * Audit Summary
  * Patient Access
  * Signed / Unsigned Notes
  * Practitioner Usage
  * Sync Issues and more

* 📱 **Responsive UI**
  Works smoothly on desktop and mobile

---

## 🧰 Tech Stack

### Backend

* FastAPI
* AWS Athena (S3 Parquet queries)
* Boto3 (AWS SDK)
* Pydantic
* Uvicorn

### Frontend

* React 18
* Vite
* Recharts
* Axios

---

## 📁 Project Structure

```
new_project/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── athena_service.py    # Athena query service
│   ├── requirements.txt
│   ├── env.example          # Environment template
│   └── verify_parquet_files.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── athena/
│   ├── create_table_ACTUAL.sql
│   ├── create_view.sql
│   └── ...
├── README.md
├── QUICK_START.md
└── SETUP.md
```

---

## 🚀 Quick Start (Local Setup)

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/infofitsoftwaresolution/Dashboard.git
cd Dashboard
```

---

## ⚙️ Backend Setup (FastAPI)

### Step 1: Go to backend folder

```bash
cd backend
```

### Step 2: Create & activate virtual environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / Mac**

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure AWS credentials

Copy `env.example` to `.env` and fill in your AWS credentials:

```bash
copy env.example .env  # Windows
cp env.example .env    # Linux/Mac
```

Edit `.env` with your AWS credentials:
```env
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_REGION=us-east-1
S3_BUCKET_NAME=your-bucket-name
S3_PREFIX=audit-trail-data/raw/
S3_RESULTS_BUCKET=your-bucket-name
S3_RESULTS_PREFIX=athena-results/
ATHENA_DATABASE_NAME=audit_trail_db
ATHENA_TABLE_NAME=audit_trail_data
ATHENA_WORKGROUP=primary
```

### Step 5: Setup Athena Table

1. Go to [AWS Athena Console](https://console.aws.amazon.com/athena/)
2. Run the SQL from `athena/create_table_ACTUAL.sql`
3. Update the S3 location to match your bucket
4. Run `MSCK REPAIR TABLE audit_trail_data;` to refresh metadata

### Step 6: Run the backend server

```bash
python main.py
```

Backend runs at:

```
http://localhost:8000
```

---

## 🎨 Frontend Setup (React)

Open a **new terminal** and:

### Step 1: Go to frontend folder

```bash
cd frontend
```

### Step 2: Install dependencies

```bash
npm install
```

### Step 3: Start development server

```bash
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

## 🌐 Open the App

Just open your browser and go to:

```
http://localhost:5173
```

---

## 🔌 API Overview

### Health & Metrics

* `GET /` – API health check
* `GET /api/metrics`
* `GET /api/top-users`
* `GET /api/active-users`

### Filters

* `GET /api/filter-options`

### Reports (supports filters)

* `/api/audit-summary`
* `/api/patient-access`
* `/api/signed-notes`
* `/api/unsigned-notes`
* `/api/practitioner-service-usage`
* `/api/sync-issues`

*All endpoints support practitioner, program, location, and date filters.*

---

## 📊 Data Source

* ☁️ **S3 Parquet Files** - All data comes from S3
* 🔍 **Athena Queries** - Direct SQL queries on Parquet files
* 📈 **Real-time** - No database, direct from S3
* 🔄 **Auto-sync** - Always shows latest data from S3

Upload your Parquet files to S3 and they'll automatically appear in the dashboard!

---

## 🐞 Common Issues & Fixes

### Backend not starting?

```bash
pip install -r requirements.txt
```

### No data showing?

1. Verify AWS credentials in `.env` file
2. Check Athena table exists: Run `SELECT COUNT(*) FROM audit_trail_data;` in Athena
3. Run `MSCK REPAIR TABLE audit_trail_data;` if you added new files
4. Verify S3 bucket permissions

### Frontend not connecting to backend?

* Make sure backend is running on `localhost:8000`
* Check browser console for CORS errors

---

## 🏗️ Production Build

### Build frontend

```bash
cd frontend
npm run build
```

Output will be in:

```
frontend/dist
```

You can serve this using FastAPI or any static server.

---

## ☁️ AWS Setup

### Required AWS Services

* **S3** - Store Parquet files
* **Athena** - Query Parquet files
* **IAM** - User with permissions for S3 and Athena

### IAM Permissions Required

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::your-bucket-name/*",
        "arn:aws:s3:::your-bucket-name"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "athena:*",
        "glue:GetDatabase",
        "glue:GetTable"
      ],
      "Resource": "*"
    }
  ]
}
```

See `QUICK_START.md` for detailed setup instructions.

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch
3. Commit changes
4. Push and open a PR

---

## 📜 License

Open‑source and free to use.

---

## 👤 Author

**infofitsoftware**

---

Happy coding! 🚀
