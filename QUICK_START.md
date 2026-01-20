# Quick Start Guide

## How to Run the Application

### Step 1: Install Dependencies
Open PowerShell or Command Prompt in the project directory and run:
```bash
pip install -r requirements.txt
```

### Step 2: Start MongoDB
Make sure MongoDB is running on your system:
- **Windows**: MongoDB should be running as a service, or start it manually
- Check if MongoDB is running: The app will connect to `mongodb://localhost:27017`

### Step 3: Run the Application
In the project directory (`E:\proj`), run:
```bash
python app.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5000
 * Running on http://0.0.0.0:5000
```

### Step 4: Access the Application
Open your web browser and go to:
```
http://localhost:5000
```
or
```
http://127.0.0.1:5000
```

## Troubleshooting

### If you see "MongoDB connection error":
1. Make sure MongoDB is installed and running
2. Check if MongoDB service is running:
   - Windows: Open Services (services.msc) and look for "MongoDB"
   - Or run: `mongod` in a separate terminal

### If port 5000 is already in use:
1. Find what's using port 5000:
   ```powershell
   netstat -ano | findstr :5000
   ```
2. Change the port in `app.py` (last line) from `port=5000` to another port like `port=5001`

### If you see import errors:
1. Make sure you're in the project directory
2. Reinstall requirements:
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

### To stop the application:
- Press `Ctrl+C` in the terminal where it's running
- Or close the terminal window

## First Time Setup

1. **Register a new account**:
   - Click "Register here" on the login page
   - Fill in all required fields:
     - Username (unique, min 3 characters)
     - Password (min 6 characters)
     - Name, Age, Gender
     - Contact Number
     - School/College Name (max 10 characters)
     - Gmail ID
   - Click "Register"

2. **Login**:
   - Use your username and password
   - Click "Login"

3. **Start using the application**:
   - Navigate to "Diagnosis" to submit a medical diagnosis
   - View your profile, history, and recommendations

## Application Features

- ✅ Secure Login/Registration
- ✅ Medical Diagnosis with ML Algorithms
- ✅ Health Recommendations
- ✅ Diagnosis History
- ✅ Emergency Alerts
- ✅ AI Chatbot
- ✅ Dark/Light Mode
- ✅ PDF/CSV Export

Enjoy using the Medical Diagnosis System!




