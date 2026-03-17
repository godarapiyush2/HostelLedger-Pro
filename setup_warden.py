from app import app, db
from models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    if not User.query.filter_by(email="warden@hostel.com").first():
        hashed_pw = generate_password_hash("warden123", method='pbkdf2:sha256')
        warden = User(
            name="Hostel Warden",
            email="warden@hostel.com",
            password=hashed_pw,
            role="Warden"
        )
        db.session.add(warden)
        db.session.commit()
        print("Warden account created successfully!")
    else:
        print("Warden account already exists.")