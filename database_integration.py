import os
import sqlite3
import pandas as pd

def integrate_database():
    print("--- Starting Database Integration ---")
    
    master_path = "data/processed/cleaned_fund_master.csv"
    history_path = "data/processed/cleaned_nav_history.csv"
    db_dir = "sql"
    db_path = os.path.join(db_dir, "mutual_funds.db")
    
    os.makedirs(db_dir, exist_ok=True)
    
    if not os.path.exists(master_path) or not os.path.exists(history_path):
        print("Error: Cleaned processed files missing! Please run data_transformation.py first.")
        return
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("Creating tables in database...")
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fund_master (
            scheme_code INTEGER PRIMARY KEY,
            scheme_name TEXT,
            fund_house TEXT,
            category TEXT,
            sub_category TEXT,
            risk_grade TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nav_history (
            scheme_code INTEGER,
            date TEXT,
            nav REAL,
            repurchase_price REAL,
            sale_price REAL,
            PRIMARY KEY (scheme_code, date)
        )
    ''')
    
    print("Loading cleaned data into DataFrames...")
    df_master = pd.read_csv(master_path)
    df_history = pd.read_csv(history_path)
    
    print("Inserting data into fund_master table...")
    df_master.to_sql('fund_master', conn, if_exists='replace', index=False)
    
    print("Inserting data into nav_history table...")
    df_history.to_sql('nav_history', conn, if_exists='replace', index=False)
    
    conn.commit()
    
    print("\n--- Verifying Database Rows ---")
    cursor.execute("SELECT COUNT(*) FROM fund_master")
    print(f"Rows in fund_master table: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM nav_history")
    print(f"Rows in nav_history table: {cursor.fetchone()[0]}")
    
    conn.close()
    print("\nSuccess: Database created and data loaded successfully at 'sql/mutual_funds.db'!")

if __name__ == "__main__":
    integrate_database() 