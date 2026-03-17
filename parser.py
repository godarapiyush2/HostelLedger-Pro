import pandas as pd

def clean_bank_statement(filepath):

    raw_df = pd.read_excel(filepath, header=None)

    header_idx = None
    for i, row in raw_df.iterrows():
        if any("date" in str(val).lower() for val in row.values):
            header_idx = i
            break

    if header_idx is None:
        raise ValueError("No Date column found in file.")

    df = pd.read_excel(filepath, skiprows=header_idx)
    df.columns = df.columns.astype(str).str.strip().str.lower()

    mapping = {}

    for col in df.columns:
        if "date" in col:
            mapping[col] = "date"
        elif "particular" in col or "desc" in col:
            mapping[col] = "description"
        elif "withdraw" in col or "debit" in col:
            mapping[col] = "debit"
        elif "deposit" in col or "credit" in col:
            mapping[col] = "credit"

    df = df.rename(columns=mapping)

    df = df.dropna(subset=["date"], how="all")

    df["debit"] = pd.to_numeric(df.get("debit", 0), errors="coerce").fillna(0)
    df["credit"] = pd.to_numeric(df.get("credit", 0), errors="coerce").fillna(0)

    df["description"] = df.get("description", "").fillna("")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    return df