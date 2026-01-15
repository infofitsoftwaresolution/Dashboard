# 🚀 Setup Guide

Complete setup instructions for running the Dashboard application.

---

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.8+** installed ([Download](https://www.python.org/downloads/))
- **Node.js 16+** and npm installed ([Download](https://nodejs.org/))
- **PostgreSQL database** (local or AWS RDS)
- **Git** installed

---

## 🔧 Step-by-Step Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/infofitsoftwaresolution/Dashboard.git
cd Dashboard
```

### Step 2: Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   
   # Linux/Mac
   python3 -m venv venv
   ```

3. **Activate virtual environment:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create environment file:**
   ```bash
   # Windows
   copy env.example .env
   
   # Linux/Mac
   cp env.example .env
   ```

6. **Configure database credentials:**
   
   Edit `backend/.env` and add your PostgreSQL credentials:
   ```env
   DB_HOST=your-database-host.rds.amazonaws.com
   DB_PORT=5432
   DB_NAME=postgres
   DB_USER=postgres
   DB_PASSWORD=your_password_here
   TABLE_NAME=audittrail_firehose
   ```

### Step 3: Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

### Step 4: Database Setup

1. **Ensure PostgreSQL database is running and accessible**

2. **Create the required table** (if it doesn't exist):
   
   Use the SQL script in `lambda/parquet_to_rds/create_rds_table.sql`
   
   Or connect to your database and run:
   ```sql
   CREATE TABLE IF NOT EXISTS audittrail_firehose (
       -- Add your table schema here
       -- See create_rds_table.sql for reference
   );
   ```

### Step 5: Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

You should see:
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

You should see:
```
VITE v5.x.x  ready in xxx ms
➜  Local:   http://localhost:5173/
```

### Step 6: Access the Dashboard

Open your browser and navigate to:
- **Dashboard:** http://localhost:5173
- **API Docs:** http://localhost:8000/docs
- **API Health:** http://localhost:8000/

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] API responds at http://localhost:8000/
- [ ] Database connection works (check http://localhost:8000/api/data/count)
- [ ] Dashboard loads at http://localhost:5173
- [ ] No errors in browser console

---

## 🐞 Troubleshooting

### Backend Issues

**Problem: ModuleNotFoundError**
- Solution: Make sure virtual environment is activated and dependencies are installed
- Run: `pip install -r requirements.txt`

**Problem: Database connection error**
- Solution: Check `.env` file has correct credentials
- Verify database is accessible from your network
- For AWS RDS: Check security group allows your IP

**Problem: Table does not exist**
- Solution: Create the table using the SQL script or update `TABLE_NAME` in `.env`

### Frontend Issues

**Problem: npm install fails**
- Solution: Make sure Node.js 16+ is installed
- Try: `npm cache clean --force` then `npm install`

**Problem: Frontend can't connect to backend**
- Solution: Verify backend is running on port 8000
- Check browser console for CORS errors
- Verify `API_BASE_URL` in frontend code

---

## 🔐 Security Notes

- ⚠️ **Never commit `.env` file to Git** - it contains sensitive credentials
- ✅ `.env` is already in `.gitignore`
- ✅ Use `env.example` as a template for required variables
- ✅ Keep database passwords secure

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Vite Documentation](https://vitejs.dev/)

---

Need help? Check the main README.md or open an issue on GitHub.

