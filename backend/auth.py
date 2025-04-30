from flask import Blueprint, request, jsonify
from models import db, User

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

# Sabit signup key
SIGNUP_SECRET_KEY = "specialhealthkey"

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    hospital = data.get('hospital')
    doctor_first_name = data.get('doctorFirstName')
    doctor_last_name = data.get('doctorLastName')
    secret_key = data.get("secret_key")

    if secret_key != SIGNUP_SECRET_KEY:
        return jsonify({"message": "Geçersiz kayıt anahtarı!"}), 403

    if not username or not password:
        return jsonify({"message": "Kullanıcı adı ve şifre gerekli."}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Bu kullanıcı adı zaten alınmış."}), 409

    new_user = User(
        username=username,
        hospital = hospital,
        doctor_first_name = doctor_first_name,
        doctor_last_name = doctor_last_name
    )
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Kayıt başarılı!"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Kullanıcı adı ve şifre gerekli."}), 400

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return jsonify({
            "message": "Giriş başarılı!",
            "username": user.username,
            "doctorFirstName": user.doctor_first_name,
            "doctorLastName": user.doctor_last_name,
            "hospital": user.hospital
        }), 200
    else:
        return jsonify({"message": "Geçersiz kullanıcı adı veya şifre."}), 401
