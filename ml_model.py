def auto_classify(description):
    
    if not description:
        return "Other"

    desc = str(description).lower()

    credit_keywords = {
        "fees": "Student Fees",
        "rent": "Rent",
        "deposit": "Security Deposit",
        "mess": "Mess Fees",
        "donation": "Donation"
    }

    debit_keywords = {
        "salary": "Salary",
        "wage": "Salary",
        "grocery": "Grocery",
        "electric": "Electricity Bill",
        "light": "Electricity Bill",
        "repair": "Maintenance",
        "plumb": "Maintenance",
        "refund": "Security Refund"
    }

    for key, value in credit_keywords.items():
        if key in desc:
            return value

    for key, value in debit_keywords.items():
        if key in desc:
            return value

    return "Other"