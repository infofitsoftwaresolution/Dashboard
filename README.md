
## ✨ What This App Can Do

* 📊 **Real‑time Dashboard Metrics**
  See key numbers at a glance with trend indicators

* 📈 **Interactive Charts**
  Line, Bar, Pie, and Area charts powered by Recharts

* 🔍 **Smart Filters**

  * Date & month range filters
  * Practitioner, Program, and Location filters
  * All updates happen instantly

* 🗄️ **Persistent Database**

  * SQLite for development
  * PostgreSQL (AWS RDS ready) for production

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
* SQLAlchemy
* SQLite / PostgreSQL
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
Dashboard/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── seed_data.py
│   ├── requirements.txt
│   └── .gitignore
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
└── README.md
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

### Step 4: Seed the database

```bash
python seed_data.py
```

✔ Creates database
✔ Creates tables
✔ Adds 1 year of sample data

### Step 5: Run the backend server

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

## 🧪 Sample Data Included

* 📆 1 year of historical data
* 👨‍⚕️ 5 practitioners
* 🏥 6 programs
* 📍 5 locations
* 📊 15,000+ records automatically generated

Perfect for demos, testing, and interviews.

---

## 🐞 Common Issues & Fixes

### Backend not starting?

```bash
pip install -r requirements.txt
```

### No data showing?

```bash
python seed_data.py
```

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

## ☁️ PostgreSQL & AWS RDS Support

The app supports **PostgreSQL for production**.

* Configure RDS security group (port 5432)
* Add credentials in `.env`
* Set `USE_POSTGRES=true`
* Seed database using:

```bash
python seed_postgresql.py
```

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
