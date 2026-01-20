"""
Profile routes
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime

bp = Blueprint('profile', __name__, url_prefix='/profile')

def init_profile_routes(app, mongo_db):
    """Initialize profile routes"""
    bp.mongo = mongo_db
    bp.app = app

@bp.route('/view')
def view():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = bp.mongo.db.users.find_one({'_id': ObjectId(session['user_id'])})
    if not user:
        session.clear()
        return redirect(url_for('auth.login'))
    
    return render_template('profile.html', user=user)

@bp.route('/update', methods=['POST'])
def update():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = bp.mongo.db.users.find_one({'_id': ObjectId(session['user_id'])})
    if not user:
        session.clear()
        return redirect(url_for('auth.login'))
    
    # Update user profile
    update_data = {
        'name': request.form.get('name'),
        'age': int(request.form.get('age', 0)),
        'gender': request.form.get('gender'),
        'contact': request.form.get('contact'),
        'medical_history': request.form.get('medical_history', ''),
        'emergency_contact': request.form.get('emergency_contact', ''),
        'updated_at': datetime.now()
    }
    
    bp.mongo.db.users.update_one(
        {'_id': ObjectId(session['user_id'])},
        {'$set': update_data}
    )
    
    flash('Profile updated successfully', 'success')
    return redirect(url_for('profile.view'))




