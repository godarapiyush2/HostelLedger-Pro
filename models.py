from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False) 
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False) # Admin, Warden, Owner

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    transactions = db.relationship('Transaction', backref='category', lazy=True)

class Transaction(db.Model):
    __tablename__ = 'transactions' 
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text)
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(20)) 
    account_type = db.Column(db.String(20))
    
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    
    note = db.Column(db.String(255))
    is_draft = db.Column(db.Boolean, default=False)