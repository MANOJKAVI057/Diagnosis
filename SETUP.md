# Setup Guide

## Prerequisites

1. **Python 3.8 or higher**
   - Download from [python.org](https://www.python.org/downloads/)

2. **MongoDB**
   - Download and install from [mongodb.com](https://www.mongodb.com/try/download/community)
   - Make sure MongoDB service is running

3. **pip** (Python package manager)
   - Usually comes with Python installation

## Installation Steps

### 1. Clone or Download the Project
```bash
cd proj
```

### 2. Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure MongoDB
- Make sure MongoDB is running on `localhost:27017`
- The database will be created automatically as `medical_diagnosis_db`

### 5. Create Environment File (Optional)
Create a `.env` file in the root directory:
```
SECRET_KEY=your-secret-key-here
MONGO_URI=mongodb://localhost:27017/medical_diagnosis_db
```

### 6. Run the Application
```bash
python app.py
```

### 7. Access the Application
Open your browser and navigate to:
```
http://localhost:5000
```

## First Time Setup

1. **Register a new account**
   - Click "Register here" on the login page
   - Fill in all required fields
   - Remember your username and password

2. **Login**
   - Use your credentials to login

3. **Submit a diagnosis**
   - Go to the Diagnosis page
   - Fill in patient information and vital signs
   - Optionally upload a medical image
   - Select an ML algorithm
   - Click Submit

## Troubleshooting

### MongoDB Connection Error
- Make sure MongoDB service is running
- Check if MongoDB is listening on port 27017
- Verify connection string in `config.py`

### Port Already in Use
- Change the port in `app.py` (last line)
- Or stop the process using port 5000

### Import Errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Verify you're using the correct Python version

### File Upload Issues
- Check that the `uploads/` directory exists
- Verify file size limits (16MB max)
- Check file format (PNG, JPG, JPEG, GIF, DICOM)

## Development Notes

- The application runs in debug mode by default
- For production, set `debug=False` in `app.py`
- Change `SECRET_KEY` in production
- Enable HTTPS and set `SESSION_COOKIE_SECURE = True` in production

## ML Models

The current implementation uses rule-based diagnosis for demonstration. To use actual trained models:

1. Train models with your medical dataset
2. Save model files in a `models/` directory
3. Update `models/ml_models.py` to load and use trained models
4. Ensure proper preprocessing of input data

## Security Notes

- Passwords are hashed using bcrypt
- Sessions are managed securely
- File uploads are validated
- Input sanitization is implemented
- In production, use environment variables for sensitive data




