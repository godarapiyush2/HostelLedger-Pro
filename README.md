# HostelLedger-Pro
A professional-grade Hostel Finance System designed for automated bank statement classification using Python and Flask. The platform features a robust MySQL-backed multi-role architecture (Admin/Warden), automated expense tracking, and real-time financial analytics to streamline hostel operations and financial transparency.

## 🚀 Features

### Bank Statement Upload
Users can upload Excel bank statements.  
The system automatically detects transaction headers and extracts:

- Date
- Description
- Debit amount
- Credit amount

### Automatic Transaction Classification
Transactions are automatically categorized using keyword detection.

Examples:
- Fees → Student Fees
- Rent → Rent
- Salary → Salary
- Electric → Electricity Bill
- Repair → Maintenance

This reduces manual classification work.

### Transaction Review System
After uploading the statement:

Users can review each transaction and classify it as:

- Personal
- Hostel Expense

Hostel expenses can be categorized using predefined categories.

### Dynamic Category Management
Wardens can manage MCQ category options.

They can:

- Add categories
- Delete categories
- Define category type (Credit or Debit)

Examples:
- Student Fees
- Grocery
- Electricity Bill
- Maintenance

### Role Based Access Control

The system supports three user roles:

Admin
- Manage wardens
- View financial analytics

Warden
- Upload bank statements
- Classify transactions
- Manage categories

### Financial Analytics Dashboard

The Admin dashboard provides:

- Total Hostel Income
- Total Hostel Expenses
- Net Profit/Loss
- Category-wise expense distribution
- Graphical charts

Charts are generated using Chart.js.

## 🛠 Technology Stack

Backend
- Python
- Flask

Database
- MySQL

Authentication
- Flask Login

Data Processing
- Pandas

Frontend
- HTML
- CSS
- Bootstrap
- JavaScript

Visualization
- Chart.js

Machine Learning (Future Feature)
- Scikit-learn

## 📂 Project Structure
project/
│
├── app.py
├── models.py
├── parser.py
├── ml_model.py
├── setup_db.py
│
├── templates/
│ ├── base.html
│ ├── login.html
│ ├── upload.html
│ ├── review.html
│ ├── classify.html
│ ├── dashboard.html
│ ├── owner.html
│ └── warden_categories.html
│
├── requirements.txt
└── README.md

## ⚙ Installation

Clone the repository

Create virtual environment

git clone https://github.com/godarapiyush2/HostelLedger-Pro.git
python -m venv venv
cd HostelLedger-Pro

Create virtual environment

python -m venv venv

Activate it

Windows

venv\Scripts\activate


Install dependencies


pip install -r requirements.txt


---

## 🗄 Database Setup

This project uses **MySQL**.

Update the database URI in `app.py`:


mysql+pymysql://username:password@localhost/hostel_finance


Create the database:


CREATE DATABASE hostel_finance;


Run setup script


python setup_db.py


This will create:

- default users
- default categories


## ▶ Run the Application


python app.py


Open in browser:


http://127.0.0.1:5000


## 🔐 Default Login Credentials

Admin  
admin@hostel.com  
admin123  

Warden  
warden@hostel.com  
warden123  


## 📈 Future Improvements

- AI-based transaction classification
- Automated anomaly detection
- PDF financial reports
- Mobile responsive dashboard
- Bank API integration

---

## 👨‍💻 Author

Developed as a financial automation system for hostel expense management.

This project demonstrates skills in:

- Python backend development
- Financial data processing
- Role based authentication
- Data visualization
