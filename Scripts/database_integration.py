import os
import sqlite3
import pandas as pd

RAW_DIR = "data/raw"
DB_PATH = "sql/mutual_funds.db"

def load_to_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    files = [f for f in os.listdir(RAW_DIR) if f.endswith('.csv') and not f.startswith('nav_')]
    
    for file in files:
        table_name = file.replace('.csv', '').strip().lower()
        file_path = os.path.join(RAW_DIR, file)
        
        df = pd.read_csv(file_path, encoding='utf-8')
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Loaded {table_name} into database.")
        
    conn.close()

if __name__ == "__main__":
    load_to_db() 