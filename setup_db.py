from app import app, db
from models import User, Category
from werkzeug.security import generate_password_hash

def create_user(name, email, password, role):
    # Check if user already exists
    if not User.query.filter_by(email=email).first():
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(name=name, email=email, password=hashed_pw, role=role)
        db.session.add(new_user)
        print(f"User created: {email} | Role: {role}")
    else:
        print(f"User {email} already exists.")

with app.app_context():
    db.create_all()

    create_user("System Admin", "admin@hostel.com", "admin123", "Admin")
    create_user("Hostel Warden", "warden@hostel.com", "warden123", "Warden")
    create_user("Hostel Owner", "owner@hostel.com", "owner123", "Owner")

    if not Category.query.first():
        default_cats = [
            ("Student Fees", "Credit"), ("Rent", "Credit"), ("Security Deposit", "Credit"),
            ("Salary", "Debit"), ("Electricity Bill", "Debit"), ("Maintenance", "Debit")
        ]
        for name, t_type in default_cats:
            db.session.add(Category(category_name=name, transaction_type=t_type, is_active=True))
        print("Default categories added.")

    db.session.commit()
    print("\nSetup Complete! You can now log in with these credentials.")