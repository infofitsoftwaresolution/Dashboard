# Quick Setup Guide

## 🚀 Fastest Way to Get Started

### Option 1: Automated Setup (Recommended)

**Windows:**
```bash
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup

Follow the detailed instructions in [README.md](README.md)

## 📋 Prerequisites Checklist

Before starting, make sure you have:

- [ ] Python 3.8 or higher installed
- [ ] Node.js 16 or higher installed
- [ ] npm (comes with Node.js)
- [ ] Git (to clone the repository)

## ✅ Verification Steps

After setup, verify everything works:

1. **Backend is running:**
   - Open: http://localhost:8000
   - Should see: `{"message":"Dashboard API is running"}`

2. **Frontend is running:**
   - Open: http://localhost:5173
   - Should see the dashboard interface

3. **Database has data:**
   - Check backend/dashboard.db exists
   - Should be ~1MB in size

## 🐛 Common Issues

### "Module not found" errors
- Make sure virtual environment is activated
- Run: `pip install -r requirements.txt` again

### "Cannot find module" in frontend
- Delete `node_modules` folder
- Run: `npm install` again

### Database is empty
- Run: `python backend/seed_data.py`

### Port already in use
- Backend: Change port in `backend/main.py` (line 792)
- Frontend: Vite will auto-use next available port

## 📞 Need Help?

1. Check the [README.md](README.md) troubleshooting section
2. Verify all prerequisites are installed
3. Check that both servers are running
4. Review browser console for errors



