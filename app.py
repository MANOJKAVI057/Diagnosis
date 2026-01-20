from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from bson import ObjectId
from datetime import datetime
import os
import bcrypt
import json
from config import Config
from models.ml_models import MLDiagnosisEngine
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import csv

app = Flask(__name__)
app.config.from_object(Config)

# Initialize MongoDB
mongo = PyMongo(app)

# Initialize ML Engine
ml_engine = MLDiagnosisEngine()

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Import routes
from routes import auth, diagnosis, profile

# Initialize routes with app and mongo
auth.init_auth_routes(app, mongo)
diagnosis.init_diagnosis_routes(app, mongo, ml_engine)
profile.init_profile_routes(app, mongo)

app.register_blueprint(auth.bp)
app.register_blueprint(diagnosis.bp)
app.register_blueprint(profile.bp)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return redirect(url_for('auth.login'))

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = mongo.db.users.find_one({'_id': ObjectId(session['user_id'])})
    if not user:
        session.clear()
        return redirect(url_for('auth.login'))
    
    # Health tips
    health_tips = [
        "Stay hydrated by drinking at least 8 glasses of water daily.",
        "Get 7-9 hours of sleep each night for optimal health.",
        "Exercise for at least 30 minutes most days of the week.",
        "Eat a balanced diet rich in fruits and vegetables.",
        "Practice stress-reduction techniques like meditation.",
        "Regular health check-ups can prevent serious conditions.",
        "Limit processed foods and sugar intake.",
        "Maintain good hygiene to prevent infections."
    ]
    import random
    daily_tip = random.choice(health_tips)
    
    return render_template('home.html', user=user, daily_tip=daily_tip)

@app.route('/help')
def help():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('help.html')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = mongo.db.users.find_one({'_id': ObjectId(session['user_id'])})
    if not user:
        session.clear()
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'delete_account':
            # Delete user account
            mongo.db.users.delete_one({'_id': ObjectId(session['user_id'])})
            mongo.db.diagnoses.delete_many({'user_id': ObjectId(session['user_id'])})
            session.clear()
            flash('Account deleted successfully', 'info')
            return redirect(url_for('auth.login'))
        elif action == 'update_theme':
            theme = request.form.get('theme', 'light')
            mongo.db.users.update_one(
                {'_id': ObjectId(session['user_id'])},
                {'$set': {'theme': theme}}
            )
            flash('Theme updated successfully', 'success')
        elif action == 'update_language':
            language = request.form.get('language', 'en')
            mongo.db.users.update_one(
                {'_id': ObjectId(session['user_id'])},
                {'$set': {'language': language}}
            )
            flash('Language updated successfully', 'success')
    
    return render_template('settings.html', user=user)

@app.route('/emergency')
def emergency():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('emergency.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    """AI Chatbot endpoint - MJ"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    message = data.get('message', '').strip().lower()
    
    if not message:
        return jsonify({'response': 'Hi! I\'m MJ. Please ask me something.'})
    
    # Simple rule-based chatbot with MJ personality
    responses = {
        'hello': 'Hello! I\'m MJ, your AI assistant. How can I help you today?',
        'hi': 'Hi there! I\'m MJ, here to assist you with the medical diagnosis system. What can I do for you?',
        'mj': 'Yes, that\'s me! I\'m MJ, your AI assistant. How can I help?',
        'help': 'I\'m MJ and I can help you with: login, registration, diagnosis submission, viewing results, and more. What do you need help with?',
        'diagnosis': 'To submit a diagnosis, go to the Diagnosis page, fill in your vital signs, upload medical images (optional), select an algorithm, and click Submit.',
        'result': 'After submitting a diagnosis, you\'ll see results on the Result page with color-coded indicators (green=normal, yellow=moderate, red=critical).',
        'emergency': 'If your diagnosis shows critical results, the Emergency Alert page will automatically open with nearby hospital information and emergency contacts.',
        'history': 'You can view all your previous diagnosis records in the History page. You can filter by vital sign or date, and export them as CSV or PDF.',
        'profile': 'Your profile page shows your personal information, age, gender, medical history, and emergency contact details. You can update it anytime.',
        'settings': 'In Settings, you can change theme (dark/light mode), select language (English/Tamil), or delete your account if needed.',
        'logout': 'Click on the Logout button in the navigation menu to safely log out of your account.',
        'register': 'To create an account, go to the Registration page and fill in: Username (unique), Password (min 6 chars), Name, Age, Gender, Contact Number, School/College Name (max 10 chars), and Gmail ID.',
        'forgot password': 'If you forgot your password, click "Forgot Password" on the login page and use your Gmail ID and School/College name to recover it.',
        'algorithm': 'You can choose from 4 ML algorithms: Logistic Regression, SVM, CNN (for images), or LSTM. Each provides different analysis approaches.',
        'normal': 'Normal results mean your vital signs are within healthy ranges. Continue monitoring and follow general health guidelines.',
        'critical': 'Critical results require immediate medical attention. The Emergency Alert page will open automatically with hospital information.',
        'thanks': 'You\'re welcome! I\'m always here to help. Is there anything else you need?',
        'thank you': 'You\'re welcome! Feel free to ask me anything else.',
        'bye': 'Goodbye! Take care of your health. I\'m here whenever you need me!'
    }
    
    # Default response
    response_text = "Hi! I'm MJ, your AI assistant. I can help you with: login, registration, diagnosis, results, emergency alerts, history, profile, settings, or general help. What would you like to know?"
    
    # Check for matching keywords
    for key, value in responses.items():
        if key in message:
            response_text = value
            break
    
    # If no match found, provide a helpful response
    if response_text == "Hi! I'm MJ, your AI assistant. I can help you with: login, registration, diagnosis, results, emergency alerts, history, profile, settings, or general help. What would you like to know?":
        # Check for partial matches
        if any(word in message for word in ['login', 'sign in', 'log in']):
            response_text = 'To login, enter your username and password on the login page. If you don\'t have an account, click "Register here" to create one.'
        elif any(word in message for word in ['register', 'sign up', 'create account']):
            response_text = 'To register, click "Register here" on the login page and fill in all required fields: Username, Password, Name, Age, Gender, Contact, School/College Name, and Gmail ID.'
        elif any(word in message for word in ['vital', 'signs', 'temperature', 'heart rate', 'blood pressure']):
            response_text = 'Vital signs include: Body Temperature, Heart Rate, Blood Pressure (systolic/diastolic), Respiratory Rate, and Oxygen Saturation. Enter these on the Diagnosis page.'
        else:
            response_text = "I'm MJ, and I'm here to help! Try asking me about: diagnosis, results, history, profile, settings, or how to use any feature of the system."
    
    return jsonify({'response': response_text})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

