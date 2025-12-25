# Verify Setup After Cloning

This guide helps you verify that the project is set up correctly after cloning.

## Quick Verification

Run the test script:

```bash
python test_setup.py
```

This will check:
- ✅ All required files exist
- ✅ Project structure is correct
- ✅ Configuration files are present
- ✅ Python and Node.js versions
- ✅ Code can be imported

## Manual Verification Steps

### 1. Check Project Structure

```bash
# Should see these directories
ls -la
# backend/
# frontend/
# athena/
```

### 2. Check Configuration

```bash
# env.example should exist
ls backend/env.example

# Copy to .env
cp backend/env.example backend/.env
# or on Windows:
copy backend\env.example backend\.env
```

### 3. Install Backend Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

**Expected output:** All packages install successfully

### 4. Install Frontend Dependencies

```bash
cd frontend
npm install
```

**Expected output:** All packages install successfully

### 5. Test Backend (without AWS credentials)

The backend should start even without AWS credentials (it will fail on API calls, but the server should start):

```bash
cd backend
python main.py
```

**Expected:** Server starts on http://localhost:8000

**Note:** API endpoints will return errors until AWS credentials are configured.

### 6. Test Frontend

```bash
cd frontend
npm run dev
```

**Expected:** Server starts on http://localhost:5173

## Common Issues

### Issue: "Module not found" errors

**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

### Issue: "npm: command not found"

**Solution:** Install Node.js from https://nodejs.org/

### Issue: Backend won't start

**Solution:**
1. Check Python version: `python --version` (need 3.8+)
2. Activate virtual environment
3. Install dependencies: `pip install -r requirements.txt`

### Issue: Frontend won't start

**Solution:**
1. Check Node.js version: `node --version` (need 16+)
2. Delete node_modules: `rm -rf node_modules`
3. Reinstall: `npm install`

### Issue: "AWS credentials must be set"

**Solution:** This is expected until you configure `.env` file. The server will start but API calls will fail.

## Full Setup Test

After configuring AWS credentials in `.env`:

1. **Start Backend:**
   ```bash
   cd backend
   python main.py
   ```

2. **Start Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Test API:**
   ```bash
   curl http://localhost:8000
   # Should return: {"message":"Dashboard API is running"}
   ```

4. **Test Frontend:**
   - Open http://localhost:5173
   - Should see the dashboard

5. **Test Athena Connection:**
   ```bash
   curl http://localhost:8000/api/athena/verify-files
   # Should return file information (if AWS is configured)
   ```

## Success Criteria

✅ All files present
✅ Dependencies install without errors
✅ Backend starts on port 8000
✅ Frontend starts on port 5173
✅ No import errors
✅ API responds (even if AWS not configured)

If all checks pass, the project is ready to use!

