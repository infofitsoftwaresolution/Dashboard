# Dashboard Application

A modern dashboard application built with React (frontend) and FastAPI (backend).

## Features

- **Real-time Metrics**: Display key performance indicators with trend indicators
- **Sales Analytics**: Interactive line chart showing sales and orders over time
- **Revenue Tracking**: Bar chart displaying monthly revenue and profit
- **User Activity**: Area chart showing hourly user activity patterns
- **Responsive Design**: Works on desktop and mobile devices

## Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── App.jsx          # Main app component
│   │   └── main.jsx         # Entry point
│   ├── package.json         # Node dependencies
│   └── vite.config.js       # Vite configuration
└── README.md
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - Windows:
   ```bash
   venv\Scripts\activate
   ```
   - Linux/Mac:
   ```bash
   source venv/bin/activate
   ```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the FastAPI server:
```bash
python main.py
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## API Endpoints

- `GET /` - API health check
- `GET /api/metrics` - Get dashboard metrics
- `GET /api/sales` - Get sales data (last 30 days)
- `GET /api/revenue` - Get monthly revenue data
- `GET /api/activity` - Get hourly user activity

## Technologies Used

### Backend
- FastAPI - Modern Python web framework
- Uvicorn - ASGI server
- Pydantic - Data validation

### Frontend
- React - UI library
- Vite - Build tool
- Recharts - Chart library
- Axios - HTTP client

## Development

The frontend is configured to proxy API requests to the backend during development. Make sure both servers are running for the full application to work.

## Production Build

To build the frontend for production:
```bash
cd frontend
npm run build
```

The built files will be in the `frontend/dist` directory.

