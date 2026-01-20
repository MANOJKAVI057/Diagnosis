"""
Diagnosis routes
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify, send_file
from flask_pymongo import PyMongo
from werkzeug.utils import secure_filename
from bson import ObjectId
from datetime import datetime
import os
from models.ml_models import MLDiagnosisEngine
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import csv
import io

bp = Blueprint('diagnosis', __name__, url_prefix='/diagnosis')

def init_diagnosis_routes(app, mongo_db, ml_engine):
    """Initialize diagnosis routes"""
    bp.mongo = mongo_db
    bp.app = app
    bp.ml_engine = ml_engine

@bp.route('/input', methods=['GET', 'POST'])
def input():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        # Get form data
        patient_name = request.form.get('name', '').strip()
        patient_age = request.form.get('age', '').strip()
        patient_contact = request.form.get('contact', '').strip()
        
        vitals = {
            'temperature': request.form.get('temperature', '98.6'),
            'heart_rate': request.form.get('heart_rate', '72'),
            'systolic_bp': request.form.get('systolic_bp', '120'),
            'diastolic_bp': request.form.get('diastolic_bp', '80'),
            'respiratory_rate': request.form.get('respiratory_rate', '16'),
            'oxygen_saturation': request.form.get('oxygen_saturation', '98')
        }
        
        algorithm = request.form.get('algorithm', 'logistic_regression')
        
        # Handle file upload
        image_path = None
        if 'medical_image' in request.files:
            file = request.files['medical_image']
            if file.filename:
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{session['user_id']}_{timestamp}_{filename}"
                image_path = os.path.join(bp.app.config['UPLOAD_FOLDER'], filename)
                file.save(image_path)
        
        # Get diagnosis
        result = bp.ml_engine.predict(algorithm, vitals, image_path)
        
        # Save diagnosis to database with patient information
        diagnosis_record = {
            'user_id': ObjectId(session['user_id']),
            'patient_name': patient_name,
            'patient_age': patient_age,
            'patient_contact': patient_contact,
            'vitals': vitals,
            'algorithm': algorithm,
            'result': result,
            'image_path': image_path,
            'created_at': datetime.now()
        }
        
        bp.mongo.db.diagnoses.insert_one(diagnosis_record)
        
        # Store result in session for result page
        session['last_diagnosis'] = {
            'condition': result['condition'],
            'severity': result['severity'],
            'confidence': result.get('confidence', 0.0),
            'algorithm': result['algorithm'],
            'vitals': vitals,
            'patient_name': patient_name,
            'patient_age': patient_age
        }
        
        # Redirect to result page
        return redirect(url_for('diagnosis.result'))
    
    return render_template('diagnosis.html')

@bp.route('/result')
def result():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if 'last_diagnosis' not in session:
        return redirect(url_for('diagnosis.input'))
    
    result_data = session['last_diagnosis']
    
    # Normal values for comparison
    normal_values = {
        'temperature': 98.6,
        'heart_rate': 72,
        'systolic_bp': 120,
        'diastolic_bp': 80,
        'respiratory_rate': 16,
        'oxygen_saturation': 98
    }
    
    # Check if critical - trigger emergency
    is_critical = result_data['severity'] == 'critical'
    
    return render_template('result.html', 
                         result=result_data, 
                         normal_values=normal_values,
                         is_critical=is_critical)

@bp.route('/comparison')
def comparison():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    # Get last diagnosis vitals
    last_diagnosis = bp.mongo.db.diagnoses.find_one(
        {'user_id': ObjectId(session['user_id'])},
        sort=[('created_at', -1)]
    )
    
    if not last_diagnosis:
        flash('No diagnosis found. Please submit a diagnosis first.', 'info')
        return redirect(url_for('diagnosis.input'))
    
    vitals = last_diagnosis['vitals']
    image_path = last_diagnosis.get('image_path')
    
    # Compare all algorithms
    comparison_results = bp.ml_engine.compare_algorithms(vitals, image_path)
    
    return render_template('comparison.html', results=comparison_results, vitals=vitals)

@bp.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    # Get filter parameters
    filter_vital = request.args.get('filter_vital')
    filter_date = request.args.get('filter_date')
    
    query = {'user_id': ObjectId(session['user_id'])}
    
    if filter_date:
        try:
            date_obj = datetime.strptime(filter_date, '%Y-%m-%d')
            query['created_at'] = {'$gte': date_obj}
        except:
            pass
    
    diagnoses = list(bp.mongo.db.diagnoses.find(query).sort('created_at', -1))
    
    # Filter by vital sign if specified
    if filter_vital:
        filtered = []
        for diag in diagnoses:
            if filter_vital in diag.get('vitals', {}):
                filtered.append(diag)
        diagnoses = filtered
    
    return render_template('history.html', diagnoses=diagnoses)

@bp.route('/export/csv')
def export_csv():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    diagnoses = list(bp.mongo.db.diagnoses.find(
        {'user_id': ObjectId(session['user_id'])}
    ).sort('created_at', -1))
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Date', 'Name', 'Age', 'Condition', 'Severity', 'Algorithm', 'Temperature', 
                    'Heart Rate', 'Systolic BP', 'Diastolic BP', 'Respiratory Rate', 
                    'Oxygen Saturation'])
    
    # Write data
    for diag in diagnoses:
        vitals = diag.get('vitals', {})
        result = diag.get('result', {})
        writer.writerow([
            diag['created_at'].strftime('%Y-%m-%d %H:%M:%S'),
            diag.get('patient_name', 'N/A'),
            diag.get('patient_age', 'N/A'),
            result.get('condition', 'N/A'),
            result.get('severity', 'N/A'),
            diag.get('algorithm', 'N/A'),
            vitals.get('temperature', 'N/A'),
            vitals.get('heart_rate', 'N/A'),
            vitals.get('systolic_bp', 'N/A'),
            vitals.get('diastolic_bp', 'N/A'),
            vitals.get('respiratory_rate', 'N/A'),
            vitals.get('oxygen_saturation', 'N/A')
        ])
    
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'diagnosis_history_{datetime.now().strftime("%Y%m%d")}.csv'
    )

@bp.route('/export/pdf/<diagnosis_id>')
def export_pdf(diagnosis_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    # Handle 'latest' case
    if diagnosis_id == 'latest':
        diagnosis = bp.mongo.db.diagnoses.find_one(
            {'user_id': ObjectId(session['user_id'])},
            sort=[('created_at', -1)]
        )
    else:
        diagnosis = bp.mongo.db.diagnoses.find_one({
            '_id': ObjectId(diagnosis_id),
            'user_id': ObjectId(session['user_id'])
        })
    
    if not diagnosis:
        flash('Diagnosis not found', 'error')
        return redirect(url_for('diagnosis.history'))
    
    # Get user information
    user = bp.mongo.db.users.find_one({'_id': ObjectId(session['user_id'])})
    
    # Create PDF
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Title
    p.setFont("Helvetica-Bold", 18)
    p.drawString(100, height - 50, "Medical Diagnosis Report")
    
    # Patient Information
    y = height - 90
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, y, "Patient Information:")
    y -= 30
    p.setFont("Helvetica", 12)
    
    # Get patient name and age from diagnosis record or user profile
    patient_name = diagnosis.get('patient_name', '')
    patient_age = diagnosis.get('patient_age', '')
    
    # If not in diagnosis, try to get from user profile
    if not patient_name and user:
        patient_name = user.get('name', 'N/A')
    if not patient_age and user:
        patient_age = str(user.get('age', 'N/A'))
    
    p.drawString(100, y, f"Name: {patient_name if patient_name else 'N/A'}")
    y -= 25
    p.drawString(100, y, f"Age: {patient_age if patient_age else 'N/A'}")
    y -= 25
    if user:
        p.drawString(100, y, f"Gender: {user.get('gender', 'N/A')}")
        y -= 25
    
    # Date
    y -= 10
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, y, f"Report Date: {diagnosis['created_at'].strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Results
    y -= 40
    result = diagnosis.get('result', {})
    vitals = diagnosis.get('vitals', {})
    
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, y, "Diagnosis Results:")
    y -= 30
    p.setFont("Helvetica", 12)
    p.drawString(100, y, f"Condition: {result.get('condition', 'N/A')}")
    y -= 25
    p.drawString(100, y, f"Severity: {result.get('severity', 'N/A')}")
    y -= 25
    p.drawString(100, y, f"Algorithm: {diagnosis.get('algorithm', 'N/A')}")
    y -= 25
    p.drawString(100, y, f"Confidence: {result.get('confidence', 0.0):.2%}")
    
    # Vital Signs
    y -= 50
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, y, "Vital Signs:")
    y -= 30
    p.setFont("Helvetica", 12)
    p.drawString(100, y, f"Temperature: {vitals.get('temperature', 'N/A')}°F")
    y -= 25
    p.drawString(100, y, f"Heart Rate: {vitals.get('heart_rate', 'N/A')} bpm")
    y -= 25
    p.drawString(100, y, f"Blood Pressure: {vitals.get('systolic_bp', 'N/A')}/{vitals.get('diastolic_bp', 'N/A')} mmHg")
    y -= 25
    p.drawString(100, y, f"Respiratory Rate: {vitals.get('respiratory_rate', 'N/A')} /min")
    y -= 25
    p.drawString(100, y, f"Oxygen Saturation: {vitals.get('oxygen_saturation', 'N/A')}%")
    
    p.save()
    buffer.seek(0)
    
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'diagnosis_report_{diagnosis_id}.pdf'
    )

@bp.route('/recommendations')
def recommendations():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    # Get last diagnosis
    last_diagnosis = bp.mongo.db.diagnoses.find_one(
        {'user_id': ObjectId(session['user_id'])},
        sort=[('created_at', -1)]
    )
    
    if not last_diagnosis:
        flash('No diagnosis found. Please submit a diagnosis first.', 'info')
        return redirect(url_for('diagnosis.input'))
    
    result = last_diagnosis.get('result', {})
    condition = result.get('condition', '').lower()
    severity = result.get('severity', 'normal')
    
    # Generate recommendations based on condition
    recommendations = {
        'diet': [],
        'exercise': [],
        'lifestyle': []
    }
    
    if 'fever' in condition:
        recommendations['diet'].append('Drink plenty of fluids and warm soups')
        recommendations['diet'].append('Eat light, easily digestible foods')
        recommendations['lifestyle'].append('Get adequate rest')
        recommendations['lifestyle'].append('Monitor temperature regularly')
    
    if 'tachycardia' in condition or 'bradycardia' in condition:
        recommendations['exercise'].append('Avoid strenuous activities')
        recommendations['exercise'].append('Practice gentle breathing exercises')
        recommendations['lifestyle'].append('Reduce stress and anxiety')
        recommendations['lifestyle'].append('Avoid caffeine and stimulants')
    
    if 'hypertension' in condition:
        recommendations['diet'].append('Reduce sodium intake')
        recommendations['diet'].append('Eat more fruits and vegetables')
        recommendations['exercise'].append('Regular moderate exercise (30 min/day)')
        recommendations['lifestyle'].append('Maintain healthy weight')
        recommendations['lifestyle'].append('Limit alcohol consumption')
    
    if 'hypotension' in condition:
        recommendations['diet'].append('Increase fluid intake')
        recommendations['diet'].append('Add moderate salt to diet')
        recommendations['lifestyle'].append('Avoid sudden position changes')
        recommendations['lifestyle'].append('Wear compression stockings if needed')
    
    # Default recommendations
    if not any(recommendations.values()):
        recommendations['diet'] = ['Maintain a balanced diet', 'Stay hydrated']
        recommendations['exercise'] = ['Regular physical activity', '30 minutes daily']
        recommendations['lifestyle'] = ['Get 7-9 hours of sleep', 'Manage stress']
    
    return render_template('recommendations.html', 
                         recommendations=recommendations,
                         condition=result.get('condition', 'Normal'),
                         severity=severity)

