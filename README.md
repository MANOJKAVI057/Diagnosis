# Machine Learning-Based Multi-Condition Diagnosis Using Medical Imaging and Physiological Data

A secure, responsive web application for medical diagnosis using machine learning algorithms.

## Features

- Secure authentication with password recovery
- Multi-condition diagnosis using ML algorithms (Logistic Regression, CNN, SVM, LSTM)
- Medical image upload (X-ray, MRI, skin images)
- Vital signs monitoring
- Emergency alert system
- Health recommendations
- Diagnosis history with export functionality
- AI chatbot assistance
- Dark/Light mode
- Multi-language support (English & Tamil)

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask
- **Database**: MongoDB
- **ML Libraries**: TensorFlow, PyTorch, Scikit-learn
- **Charts**: Chart.js

## Setup Instructions

### Prerequisites

- Python 3.8+
- MongoDB installed and running
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd proj
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up MongoDB:
   - Make sure MongoDB is running on `localhost:27017`
   - The database will be created automatically as `medical_diagnosis_db`

4. Configure environment variables:
   - Create a `.env` file in the root directory (optional, defaults are provided)

5. Run the application:
```bash
python app.py
```

6. Open your browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
proj/
├── app.py                 # Flask application entry point
├── config.py             # Configuration settings
├── models/
│   ├── __init__.py
│   ├── user_model.py     # User data models
│   └── ml_models.py      # ML model implementations
├── routes/
│   ├── __init__.py
│   ├── auth.py           # Authentication routes
│   ├── diagnosis.py      # Diagnosis routes
│   └── profile.py        # User profile routes
├── static/
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   ├── js/
│   │   ├── main.js       # Main JavaScript
│   │   └── chatbot.js    # Chatbot functionality
│   └── images/           # Static images
├── templates/
│   ├── base.html         # Base template
│   ├── login.html        # Login/Registration page
│   ├── home.html         # Home page
│   ├── profile.html      # User profile page
│   ├── diagnosis.html    # Diagnosis input page
│   ├── result.html       # Diagnosis result page
│   ├── emergency.html    # Emergency alert page
│   ├── recommendations.html  # Health recommendations
│   ├── history.html      # Diagnosis history
│   ├── help.html         # Help page
│   ├── settings.html     # Settings page
│   └── comparison.html   # Algorithm comparison page
└── uploads/              # Uploaded medical images
```

## Usage

1. **Registration**: Create a new account with your details
2. **Login**: Use your username and password to login
3. **Diagnosis**: Upload medical images and enter vital signs
4. **Results**: View diagnosis results with color-coded indicators
5. **History**: Access your previous diagnosis records
6. **Settings**: Customize theme and language preferences

## Security Features

- Password hashing using bcrypt
- Session management
- Secure file uploads
- Input validation

## License

This project is for educational purposes.

