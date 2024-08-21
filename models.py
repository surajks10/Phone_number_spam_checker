from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)
    contacts = db.relationship('Contact', backref='owner', lazy=True)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    is_spam = db.Column(db.Boolean, default=False)

class SpamReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(15), nullable=False)
    reported_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

