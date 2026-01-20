"""
User data models and validation
"""

from datetime import datetime

def validate_user_data(data):
    """Validate user registration data"""
    errors = []
    
    if not data.get('username') or len(data['username']) < 3:
        errors.append('Username must be at least 3 characters')
    
    if not data.get('password') or len(data['password']) < 6:
        errors.append('Password must be at least 6 characters')
    
    if not data.get('name'):
        errors.append('Name is required')
    
    if not data.get('age') or not data['age'].isdigit():
        errors.append('Valid age is required')
    
    if not data.get('contact'):
        errors.append('Contact number is required')
    
    if not data.get('school_college') or len(data['school_college']) > 10:
        errors.append('School/College name is required (max 10 characters)')
    
    if not data.get('gmail'):
        errors.append('Gmail ID is required')
    
    return errors

def create_user_dict(data, hashed_password):
    """Create user document for MongoDB"""
    return {
        'username': data['username'],
        'password': hashed_password,
        'name': data['name'],
        'age': int(data['age']),
        'gender': data.get('gender', 'Not specified'),
        'contact': data['contact'],
        'school_college': data['school_college'],
        'gmail': data['gmail'],
        'medical_history': data.get('medical_history', ''),
        'emergency_contact': data.get('emergency_contact', ''),
        'theme': 'light',
        'language': 'en',
        'created_at': datetime.now(),
        'updated_at': datetime.now()
    }

