# HostelLedger-Pro
A professional-grade Hostel Finance System designed for automated bank statement classification using Python and Flask. The platform features a robust MySQL-backed multi-role architecture (Admin/Warden), automated expense tracking, and real-time financial analytics to streamline hostel operations and financial transparency.

# 🌟 The Problem & Solution
Traditional hostel management relies on manual entry of bank statements into spreadsheets, which is time-consuming and prone to error. This project solves that by:
1. **Automating Classification:** Using Python logic to distinguish between Hostel and Personal expenses.
2. **Centralizing Data:** Replacing fragmented files with a robust MySQL relational database.
3. **Role-Specific Dashboards:** Ensuring Admin, Warden, and Owner see only the data relevant to them.

# ✨ Key Features
* **Bank Statement Processor:** Upload Excel/CSV statements; the system uses `Pandas` to parse and categorize transactions instantly.
* **Automated Expense Classification:** Logic-based filtering that identifies hostel-related costs versus personal withdrawals.
* **Multi-Role RBAC (Role-Based Access Control):**
    * **Admin:** Full access to user management and system audits.
    * **Warden:** Access to daily expense logging and transaction uploads.
* **Real-time Analytics:** Visualized financial health, monthly spending trends, and budget alerts.
* **Secure Database:** Integrated MySQL backend for handling high-concurrency and persistent data storage.

# 🛠️ Tech Stack
* **Backend:** Python 3.x, Flask
* **Database:** MySQL (Relational Schema)
* **Data Processing:** Pandas, OpenPyXL
* **Frontend:** Jinja2 Templates, Bootstrap 5
* **Security:** Werkzeug (Password Hashing), Environment Variables (.env)

# ⚙️ Installation & Setup

### 1. Database Setup
Create a MySQL database and run the following schema:
```sql
CREATE DATABASE hostel_finance;
-- Import schema.sql from the /db folder

