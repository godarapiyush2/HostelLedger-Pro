import os
import pandas as pd
from io import BytesIO
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy import func, extract

from models import db, User, Category, Transaction
from parser import clean_bank_statement
from ml_model import auto_classify

app = Flask(__name__)
app.secret_key = "hardworking_hostel_secret_key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:4306/hostel_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            if user.role == 'Admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('upload_file'))
        flash("Invalid email or password", "danger")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/warden/categories', methods=['GET', 'POST'])
@login_required
def manage_categories():
    if request.method == 'POST':
        name = request.form.get('category_name')
        t_type = request.form.get('transaction_type')
        if name:
            new_cat = Category(category_name=name, transaction_type=t_type, is_active=True)
            db.session.add(new_cat)
            db.session.commit()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({"status": "success"})
            flash("Category added successfully", "success")
            return redirect(url_for('manage_categories'))
            
    categories = Category.query.all()
    return render_template('warden_categories.html', categories=categories)

@app.route('/warden/delete_category/<int:id>')
@login_required
def delete_category(id):
    category = db.session.get(Category, id)
    if category:
        db.session.delete(category)
        db.session.commit()
        flash("Category deleted", "warning")
    return redirect(url_for('manage_categories'))


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            try:
                df = clean_bank_statement(filepath)
                entries = []
                for _, row in df.iterrows():
                    raw_date = row['date']
                    clean_date = raw_date.strftime('%Y-%m-%d') if hasattr(raw_date, 'strftime') else str(raw_date).split(' ')[0]

                    entries.append({
                        'date': clean_date,
                        'description': row.get('description', 'N/A'),
                        'debit': float(row.get('debit', 0)),
                        'credit': float(row.get('credit', 0)),
                        'suggested_category': auto_classify(row.get("description", ""))
                    })
                categories = Category.query.filter_by(is_active=True).all()
                return render_template('review.html', transactions=entries, categories=categories)
            except Exception as e:
                flash(f"Excel Error: {str(e)}", "danger")
    return render_template('upload.html')

@app.route('/save_bulk_transactions', methods=['POST'])
@login_required
def save_bulk():
    action = request.form.get('action')
    dates = request.form.getlist('date[]')
    descriptions = request.form.getlist('description[]')
    amounts = request.form.getlist('amount[]')
    types = request.form.getlist('type[]')
    accounts = request.form.getlist('account_type[]')
    category_ids = request.form.getlist('category_id[]')
    notes = request.form.getlist('note[]')

    try:
        for i in range(len(dates)):
            cat_id = category_ids[i] if (i < len(category_ids) and category_ids[i]) else None
            new_txn = Transaction(
                date=datetime.strptime(dates[i], '%Y-%m-%d').date(),
                description=descriptions[i],
                amount=float(amounts[i]),
                transaction_type=types[i],
                account_type=accounts[i],
                category_id=int(cat_id) if cat_id and cat_id != "" else None,
                note=notes[i],
                is_draft=(action == 'save_draft')
            )
            db.session.add(new_txn)
        db.session.commit()
        flash("Work saved successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Database Save Error: {str(e)}", "danger")

    return redirect(url_for('owner_analytics'))


@app.route('/export_excel')
@login_required
def export_excel():
    txns = Transaction.query.all()
    data = []
    for t in txns:
        cat_name = "Personal"
        if t.category_id:
            cat_obj = db.session.get(Category, t.category_id)
            if cat_obj:
                cat_name = cat_obj.category_name
        
        data.append({
            "Date": t.date.strftime('%d-%b-%Y') if hasattr(t.date, 'strftime') else t.date,
            "Description": t.description,
            "Amount": t.amount,
            "Type": t.transaction_type,
            "Account": t.account_type,
            "Category": cat_name,
            "Note": t.note
        })

    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return send_file(output, download_name=f"Hostel_Report_{date.today()}.xlsx", as_attachment=True)


@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'Admin': return "Access Denied", 403
    wardens = User.query.filter_by(role='Warden').all()
    return render_template('admin_dashboard.html', wardens=wardens)

@app.route('/admin/add_warden', methods=['GET', 'POST'])
@login_required
def add_warden():
    if current_user.role != 'Admin': return "Access Denied", 403
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        if User.query.filter_by(email=email).first():
            flash("Warden already exists", "danger")
            return redirect(url_for('add_warden'))
        new_warden = User(name=name, email=email, password=generate_password_hash(password), role='Warden')
        db.session.add(new_warden)
        db.session.commit()
        flash("Warden created!", "success")
        return redirect(url_for('admin_dashboard'))
    return render_template('add_warden.html')

@app.route('/admin/delete_warden/<int:id>')
@login_required
def delete_warden(id):
    if current_user.role != 'Admin': return "Access Denied", 403
    user = db.session.get(User, id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash("Warden deleted", "warning")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/analytics')
@login_required
def owner_analytics():
    if current_user.role != 'Admin':
        flash("Unauthorized Access", "danger")
        return redirect(url_for('upload_file'))

    income = db.session.query(func.sum(Transaction.amount)).filter(Transaction.account_type == 'Hostel', Transaction.transaction_type == 'Credit').scalar() or 0
    expense = db.session.query(func.sum(Transaction.amount)).filter(Transaction.account_type == 'Hostel', Transaction.transaction_type == 'Debit').scalar() or 0
    category_data = db.session.query(Category.category_name, func.sum(Transaction.amount)).join(Transaction).filter(Transaction.account_type == 'Hostel', Transaction.transaction_type == 'Debit').group_by(Category.category_name).all()

    labels = [r[0] for r in category_data]
    values = [float(r[1]) for r in category_data]

    return render_template('owner.html', income=income, expense=expense, profit=income - expense, labels=labels, values=values)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(email='admin@hostel.com').first():
            admin = User(name='Super Admin', email='admin@hostel.com', password=generate_password_hash('admin123'), role='Admin')
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)