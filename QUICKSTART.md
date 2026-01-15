# ⚡ Quick Start Guide

Get the Dashboard running in 5 minutes!

---

## 🚀 Quick Setup

### 1. Clone and Setup Backend

```bash
git clone https://github.com/infofitsoftwaresolution/Dashboard.git
cd Dashboard/backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy env.example .env  # Windows
# cp env.example .env  # Linux/Mac
```

### 2. Configure Database

Edit `backend/.env` and add your PostgreSQL credentials:

```env
DB_HOST=your-database-host.rds.amazonaws.com
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_password_here
TABLE_NAME=audittrail_firehose
```

### 3. Setup Frontend

```bash
cd ../frontend
npm install
```

### 4. Run Application

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 5. Open Dashboard

- **Dashboard:** http://localhost:5173
- **API Docs:** http://localhost:8000/docs

---

## ✅ Verify Setup

Run the test script to verify everything is configured:

```bash
cd backend
python test_setup.py
```

---

## 🆘 Need Help?

- See **README.md** for detailed documentation
- See **SETUP.md** for step-by-step instructions
- Check **Troubleshooting** section in README.md

---

That's it! 🎉

