"""
Authentication routes
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt
from bson import ObjectId
from datetime import datetime
from models.user_model import validate_user_data, create_user_dict

bp = Blueprint('auth', __name__, url_prefix='/auth')

def init_auth_routes(app, mongo_db):
    """Initialize auth routes with app and mongo instances"""
    bp.mongo = mongo_db
    bp.app = app

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please enter both username and password', 'error')
            return render_template('login.html')
        
        user = bp.mongo.db.users.find_one({'username': username})
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            session['user_id'] = str(user['_id'])
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        data = request.form.to_dict()
        
        # Validate data
        errors = validate_user_data(data)
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('login.html', register_mode=True)
        
        # Check if username exists
        if bp.mongo.db.users.find_one({'username': data['username']}):
            flash('Username already exists. Please choose another.', 'error')
            return render_template('login.html', register_mode=True)
        
        # Check if email exists
        if bp.mongo.db.users.find_one({'gmail': data['gmail']}):
            flash('Gmail ID already registered', 'error')
            return render_template('login.html', register_mode=True)
        
        # Hash password
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        
        # Create user
        user_dict = create_user_dict(data, hashed_password)
        result = bp.mongo.db.users.insert_one(user_dict)
        
        if result.inserted_id:
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Registration failed. Please try again.', 'error')
    
    return render_template('login.html', register_mode=True)

@bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        gmail = request.form.get('gmail')
        school_college = request.form.get('school_college')
        
        if not gmail or not school_college:
            flash('Please enter both Gmail ID and School/College name', 'error')
            return render_template('forgot_password.html')
        
        user = bp.mongo.db.users.find_one({
            'gmail': gmail,
            'school_college': school_college
        })
        
        if user:
            # In production, send password reset email
            # For demo, show success message
            flash('Password recovery information sent to your email. (Demo: Check your email for reset link)', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('No account found with the provided Gmail ID and School/College name', 'error')
    
    return render_template('forgot_password.html')

@bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect(url_for('auth.login'))




