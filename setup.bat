@echo off
REM Dashboard Project Setup Script for Windows
REM This script sets up both backend and frontend

echo ==========================================
echo Dashboard Project Setup
echo ==========================================

REM Check if Python is installed
echo.
echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo [OK] Python found

REM Check if Node.js is installed
echo.
echo Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)
node --version
echo [OK] Node.js found

REM Check if npm is installed
npm --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] npm is not installed
    pause
    exit /b 1
)
npm --version
echo [OK] npm found

REM Setup Backend
echo.
echo ==========================================
echo Setting up Backend...
echo ==========================================
cd backend

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install Python dependencies
echo Installing Python dependencies...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install Python dependencies
    pause
    exit /b 1
)
echo [OK] Python dependencies installed

REM Seed database
echo Seeding database...
python seed_data.py
if errorlevel 1 (
    echo [ERROR] Failed to seed database
    pause
    exit /b 1
)
echo [OK] Database seeded successfully

deactivate
cd ..

REM Setup Frontend
echo.
echo ==========================================
echo Setting up Frontend...
echo ==========================================
cd frontend

REM Install Node dependencies
echo Installing Node dependencies...
call npm install --silent
if errorlevel 1 (
    echo [ERROR] Failed to install Node dependencies
    pause
    exit /b 1
)
echo [OK] Node dependencies installed

cd ..

echo.
echo ==========================================
echo [OK] Setup Complete!
echo ==========================================
echo.
echo To start the application:
echo.
echo Terminal 1 (Backend):
echo   cd backend
echo   venv\Scripts\activate
echo   python main.py
echo.
echo Terminal 2 (Frontend):
echo   cd frontend
echo   npm run dev
echo.
echo Then open: http://localhost:5173
echo.
pause



