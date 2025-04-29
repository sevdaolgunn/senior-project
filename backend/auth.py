from flask import Blueprint, request, jsonify, current_app
from models import db, User
import jwt
import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 409
    new_user = User(username=data['username'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, current_app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401
