from flask import Flask, request, jsonify, render_template, send_from_directory
from models import db, init_db, User
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
init_db(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard.html')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # In a real app, verify password hash. Here we just check existence as per spec.
    user = User.query.filter_by(username=username).first()
    
    if user and user.password_hash == password: # Simulating password check
        return jsonify({"token": user.api_token, "message": "Login Successful"})
    
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/api/dashboard-data', methods=['GET'])
def dashboard_data():
    token = request.headers.get('Authorization')
    user = User.query.filter_by(api_token=token).first()
    
    if not user:
        return jsonify({"message": "Unauthorized"}), 401
    
    image_url = "/static/img/employee.svg"
    if user.role == 'admin':
        image_url = "/static/img/admin_secret.svg"
        
    return jsonify({
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "dashboard_image": image_url
    })

@app.route('/api/profile/update', methods=['POST'])
def update_profile_vulnerable():
    token = request.headers.get('Authorization')
    user = User.query.filter_by(api_token=token).first()
    
    if not user:
        return jsonify({"message": "Unauthorized"}), 401
        
    data = request.get_json()
    
    # VULNERABLE IMPLEMENTATION: Mass Assignment (PATCHED)
    # for key, value in data.items():
    #     # Intentionally allowing all keys to be updated
    #     if hasattr(user, key):
    #         setattr(user, key, value)

    # SECURE IMPLEMENTATION: Whitelist approach
    if 'email' in data:
        user.email = data['email']
            
    db.session.commit()
    return jsonify({"message": "Profile updated successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
