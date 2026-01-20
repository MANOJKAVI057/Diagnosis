# Project Summary

## Machine Learning-Based Multi-Condition Diagnosis Using Medical Imaging and Physiological Data

A comprehensive, secure web application for medical diagnosis using multiple ML algorithms.

## Features Implemented

### ✅ Authentication System
- Secure login and registration
- Unique username validation
- Password recovery using Gmail + School/College name
- Password hashing with bcrypt
- Session management

### ✅ Pages & Functionality

1. **Login/Registration Page**
   - Secure authentication
   - Forgot password option
   - User registration with all required fields

2. **Home Page**
   - Navigation to all pages
   - Welcome message with user name
   - Random health tips on refresh
   - Emergency contact information
   - Quick action cards

3. **User Profile Page**
   - Display and update personal information
   - Medical history
   - Emergency contact details

4. **Diagnosis Input Page**
   - Patient information form
   - Vital signs input (Temperature, Heart Rate, BP, etc.)
   - Medical image upload (X-ray, MRI, skin images)
   - Algorithm selection (Logistic Regression, CNN, SVM, LSTM)

5. **Diagnosis Result Page**
   - Color-coded results (Green=Normal, Red=Critical)
   - Comparison chart (normal vs current values)
   - Downloadable PDF health report
   - Auto-trigger Emergency Alert for critical results

6. **Emergency Alert Page**
   - Emergency warning popup
   - Nearby hospitals list
   - Emergency call buttons
   - Emergency information

7. **Health Recommendation Page**
   - Personalized diet suggestions
   - Exercise recommendations
   - Lifestyle modifications
   - Based on diagnosis results

8. **History Page**
   - View all previous diagnosis records
   - Filter by vital sign and date
   - Export as CSV or PDF

9. **Help Page**
   - Step-by-step user guide
   - Feature explanations
   - Troubleshooting tips

10. **Settings Page**
    - Dark/Light mode toggle
    - Language selection (English & Tamil)
    - Delete account option

11. **Algorithm Comparison Page**
    - Compare results from all algorithms
    - Performance graphs
    - Confidence comparison

### ✅ AI Chatbot
- Available on all pages (bottom-right corner)
- Provides greetings and guidance
- Form assistance
- Usage help

### ✅ Security Features
- Password hashing with bcrypt
- Session management
- Secure file uploads
- Input validation
- CSRF protection ready

### ✅ Additional Features
- Responsive design
- Dark/Light mode
- Multi-language support (English/Tamil ready)
- PDF report generation
- CSV export
- Chart.js integration for visualizations

## Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Flask (Python)
- **Database**: MongoDB with PyMongo
- **ML Libraries**: 
  - Scikit-learn (Logistic Regression, SVM)
  - TensorFlow (CNN support)
  - PyTorch (LSTM support)
- **Charts**: Chart.js
- **PDF Generation**: ReportLab
- **Security**: bcrypt, Werkzeug

## Project Structure

```
proj/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── README.md            # Main documentation
├── SETUP.md            # Setup instructions
├── DATABASE_SCHEMA.md  # Database structure
├── models/             # Data models
│   ├── user_model.py   # User validation
│   └── ml_models.py    # ML model implementations
├── routes/             # Route handlers
│   ├── auth.py         # Authentication routes
│   ├── diagnosis.py    # Diagnosis routes
│   └── profile.py      # Profile routes
├── templates/          # HTML templates
│   ├── base.html       # Base template
│   ├── login.html      # Login/Registration
│   ├── home.html       # Home page
│   ├── profile.html    # User profile
│   ├── diagnosis.html  # Diagnosis input
│   ├── result.html     # Results page
│   ├── emergency.html  # Emergency alert
│   ├── recommendations.html  # Health tips
│   ├── history.html    # Diagnosis history
│   ├── comparison.html # Algorithm comparison
│   ├── help.html       # Help page
│   └── settings.html   # Settings page
├── static/             # Static files
│   ├── css/
│   │   └── style.css   # Main stylesheet
│   └── js/
│       ├── main.js     # Main JavaScript
│       └── chatbot.js  # Chatbot functionality
└── uploads/           # Uploaded medical images
```

## Database Collections

1. **users**: User accounts and profiles
2. **diagnoses**: Diagnosis records and results

## ML Algorithms

1. **Logistic Regression**: For binary classification
2. **SVM**: Support Vector Machine for classification
3. **CNN**: Convolutional Neural Network for image analysis
4. **LSTM**: Long Short-Term Memory for sequential data

## Security Implementation

- Passwords hashed with bcrypt
- Session-based authentication
- File upload validation
- Input sanitization
- Secure cookie settings

## Future Enhancements

- Real ML model training and deployment
- Integration with actual hospital APIs
- Real-time map integration for hospitals
- Email notifications
- Multi-language translations (Tamil)
- Advanced image processing
- Real-time vital signs monitoring
- Integration with wearable devices

## Notes

- Current ML models use rule-based logic for demonstration
- In production, replace with trained models
- Add proper error handling and logging
- Implement rate limiting for API endpoints
- Add comprehensive testing
- Set up CI/CD pipeline




