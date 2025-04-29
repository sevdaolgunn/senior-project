from flask import Flask
from flask_cors import CORS
from models import db
from auth import auth_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your-secret-key'

db.init_app(app)
CORS(app)
app.register_blueprint(auth_bp)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
