from werkzeug.security import generate_password_hash
admin_user = User(
    name="Admin", 
    email="admin@hostel.com", 
    password=generate_password_hash("admin123", method='pbkdf2:sha256'), 
    role="Admin"
)