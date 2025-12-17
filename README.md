# Dashboard Application

A comprehensive healthcare dashboard application built with React (frontend) and FastAPI (backend), featuring SQLite database, real-time filtering, and interactive data visualizations.

## Features

- **Real-time Metrics Dashboard**: Key performance indicators with trend indicators
- **Interactive Charts**: Multiple chart types (Line, Bar, Pie, Area) using Recharts
- **Advanced Filtering**: 
  - Date range and month range filtering
  - Practitioner, Program, and Location filters
  - Real-time data updates
- **SQLite Database**: Persistent data storage with one year of sample data
- **Multiple Report Sections**: 
  - Audit Summary
  - Patient Access
  - Signed/Unsigned Notes
  - Practitioner Usage
  - Sync Issues
  - And more...
- **Responsive Design**: Works on desktop and mobile devices

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 16+** and npm - [Download Node.js](https://nodejs.org/)
- **Git** - [Download Git](https://git-scm.com/downloads)

## Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application
│   ├── database.py          # SQLAlchemy models and database setup
│   ├── seed_data.py         # Database seeding script
│   ├── requirements.txt     # Python dependencies
│   └── .gitignore           # Backend gitignore
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── App.jsx          # Main app component
│   │   └── main.jsx         # Entry point
│   ├── package.json         # Node dependencies
│   └── vite.config.js       # Vite configuration
└── README.md
```

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Shubham96681/Dashboard.git
cd Dashboard
```

### 2. Backend Setup

#### Step 1: Navigate to backend directory
```bash
cd backend
```

#### Step 2: Create a virtual environment (recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Python dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Initialize and seed the database
```bash
python seed_data.py
```

This will:
- Create the SQLite database (`dashboard.db`)
- Create all necessary tables
- Populate the database with one year of sample data

**Expected output:**
```
Database seeded successfully!
```

#### Step 5: Start the FastAPI server
```bash
python main.py
```

The backend will be available at `http://localhost:8000`

**You should see:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### 3. Frontend Setup

Open a **new terminal window** (keep the backend running) and:

#### Step 1: Navigate to frontend directory
```bash
cd frontend
```

#### Step 2: Install Node dependencies
```bash
npm install
```

This may take a few minutes on first run.

#### Step 3: Start the development server
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

**You should see:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### 4. Access the Application

Open your browser and navigate to:
```
http://localhost:5173
```

## Troubleshooting

### Backend Issues

**Problem: `ModuleNotFoundError` or `No module named 'fastapi'`**
```bash
# Make sure virtual environment is activated
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

**Problem: `database.db` not found or empty**
```bash
# Run the seed script
python seed_data.py
```

**Problem: Port 8000 already in use**
```bash
# Option 1: Stop the process using port 8000
# Option 2: Change port in main.py (last line)
#   uvicorn.run(app, host="0.0.0.0", port=8001)
```

### Frontend Issues

**Problem: `npm: command not found`**
- Install Node.js from [nodejs.org](https://nodejs.org/)

**Problem: `node_modules` errors**
```bash
# Delete node_modules and reinstall
rm -rf node_modules  # Linux/Mac
rmdir /s node_modules  # Windows
npm install
```

**Problem: Port 5173 already in use**
```bash
# Vite will automatically use the next available port
# Or specify a different port:
npm run dev -- --port 3000
```

**Problem: Cannot connect to backend API**
- Make sure the backend is running on `http://localhost:8000`
- Check browser console for CORS errors
- Verify backend is accessible: `http://localhost:8000/`

### Database Issues

**Problem: Database is empty or shows no data**
```bash
cd backend
python seed_data.py
```

**Problem: Database locked error**
- Close any other processes accessing the database
- Restart the backend server

## API Endpoints

### Dashboard Endpoints
- `GET /` - API health check
- `GET /api/metrics` - Get dashboard metrics
- `GET /api/top-users` - Get top users
- `GET /api/active-users` - Get active users count
- `GET /api/staff-speaking` - Get staff speaking data
- `GET /api/times` - Get time metrics
- `GET /api/consents` - Get consents data

### Filter Endpoints
- `GET /api/filter-options` - Get available filter options (practitioners, programs, locations)

### Report Endpoints (with filtering support)
- `GET /api/audit-summary?practitioner=...&program=...&location=...&start_date=...&end_date=...`
- `GET /api/patient-access?practitioner=...&program=...&location=...&start_date=...&end_date=...`
- `GET /api/signed-notes?practitioner=...&program=...&location=...&start_date=...&end_date=...`
- `GET /api/unsigned-notes?practitioner=...&program=...&location=...&start_date=...&end_date=...`
- `GET /api/practitioner-service-usage?practitioner=...&program=...&location=...`
- `GET /api/sync-issues?start_date=...&end_date=...`
- And more...

## Technologies Used

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **SQLite** - Lightweight database
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation

### Frontend
- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Recharts** - Chart library
- **Axios** - HTTP client

## Development

### Running Both Servers

You need to run both backend and frontend servers simultaneously:

**Terminal 1 (Backend):**
```bash
cd backend
venv\Scripts\activate  # or source venv/bin/activate on Linux/Mac
python main.py
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

### Making Changes

- **Backend changes**: Restart the FastAPI server (`Ctrl+C` then `python main.py`)
- **Frontend changes**: Vite will hot-reload automatically

## Production Build

### Build Frontend
```bash
cd frontend
npm run build
```

The built files will be in the `frontend/dist` directory.

### Serve Frontend with Backend
You can serve the built frontend files using the FastAPI backend or any static file server.

## Database

The application supports both **SQLite** (default for development) and **PostgreSQL** (for production/AWS RDS).

### Database Migration

To migrate from SQLite to PostgreSQL (AWS RDS), see the [Migration Guide](backend/MIGRATION_GUIDE.md).

**Quick Migration:**
```bash
cd backend
python migrate_to_postgres.py
# Or use the interactive version:
python quick_migrate.py
```

### Database Schema

The application uses the following main tables:
- `metrics` - Dashboard metrics
- `top_users` - Top users data
- `audit_items` - Audit log entries
- `patient_access_items` - Patient access records
- `signed_note_items` - Signed notes
- `unsigned_note_items` - Unsigned notes
- `practitioner_usage_items` - Practitioner usage statistics
- And more...

## Filtering Features

### Date/Month Range Filtering
- Select "Last 3 Months" for quick filter
- Use calendar icon to select custom date or month ranges
- All charts and tables update in real-time

### Practitioner/Program/Location Filtering
- Click Practitioner/Program/Location buttons
- Select from dropdown menus
- Multiple filters can be combined
- Clear individual filters or all at once

## Sample Data

The database is seeded with:
- **One year** of historical data
- **5 Practitioners** with distinct data patterns:
  - DR JANE SMITH (Cardiology) - 4,791 notes
  - DR JOHN DOE (Pediatrics) - 3,168 notes
  - DR SARAH JOHNSON (Orthopedics/Neurology) - 5,526 notes
  - DR MICHAEL BROWN (Dermatology) - 2,535 notes
  - DR EMILY DAVIS (Neurology/Cardiology) - 3,619 notes
- **6 Programs**: Cardiology, Primary Care, Pediatrics, Orthopedics, Neurology, Dermatology
- **5 Locations**: Main Clinic, Downtown Office, North Branch, South Branch, Emergency Dept

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is open source and available for use.

## Support

If you encounter any issues:
1. Check the Troubleshooting section above
2. Verify all prerequisites are installed
3. Ensure both backend and frontend servers are running
4. Check browser console for errors
5. Verify database was seeded successfully

## Author

Shubham96681

---

**Happy Coding! 🚀**
