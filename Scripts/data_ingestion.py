import os
import pandas as pd

RAW_DIR = "data/raw"

def ingest_data():
    if not os.path.exists(RAW_DIR):
        return
        
    files = sorted([f for f in os.listdir(RAW_DIR) if f.endswith('.csv')])
    
    for file in files:
        if file.startswith("nav_"):
            continue
            
        file_path = os.path.join(RAW_DIR, file)
        df = pd.read_csv(file_path, encoding='utf-8')
        
        print(f"File: {file}")
        print(f"Shape: {df.shape}")
        print("Dtypes:")
        print(df.dtypes)
        print("Head:")
        print(df.head(3))
        print("-" * 40)

if __name__ == "__main__":
    ingest_data()