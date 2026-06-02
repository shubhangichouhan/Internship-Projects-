import os
import sqlite3
import pandas as pd

DB_PATH = "sql/mutual_funds.db"
PROCESSED_DIR = "data/processed"

def transform_and_explore():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    if not os.path.exists(DB_PATH):
        return
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall()]
    
    fund_table = [t for t in tables if "fund_master" in t]
    nav_table = [t for t in tables if "nav_history" in t]
    
    if fund_table:
        df_master = pd.read_sql(f"SELECT * FROM [{fund_table[0]}]", conn)
        print("=== EXPLORING FUND MASTER ===")
        print(f"Unique Fund Houses (Top 5): {df_master.iloc[:, 1].dropna().unique()[:5]}")
        print(f"Unique Categories: {df_master.iloc[:, 2].dropna().unique()[:5]}")
        print(f"Risk Grades Found: {df_master.iloc[:, 4].dropna().unique() if df_master.shape[1] > 4 else 'N/A'}")
        print("-" * 50)

    if fund_table and nav_table:
        df_master = pd.read_sql(f"SELECT * FROM [{fund_table[0]}]", conn)
        df_nav = pd.read_sql(f"SELECT * FROM [{nav_table[0]}]", conn)
        master_codes = set(df_master.iloc[:, 0].dropna().unique())
        nav_codes = set(df_nav.iloc[:, 0].dropna().unique())
        missing_codes = master_codes - nav_codes
        
        print("=== DATA QUALITY SUMMARY ===")
        print(f"Total AMFI Codes in Fund Master: {len(master_codes)}")
        print(f"Total AMFI Codes in NAV History: {len(nav_codes)}")
        print(f"Mismatch/Missing Codes Count: {len(missing_codes)}")
        print(f"Data Quality Status: {'PASSED' if len(missing_codes) == 0 else 'WARNING: Code Mismatch Found'}")
        print("-" * 50)

    for table in tables:
        df = pd.read_sql(f"SELECT * FROM [{table}]", conn)
        df_cleaned = df.dropna(how='all')
        df_cleaned.to_csv(os.path.join(PROCESSED_DIR, f"cleaned_{table}.csv"), index=False)
        
    conn.close()

if __name__ == "__main__": 
    transform_and_explore()