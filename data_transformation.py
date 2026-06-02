import os
import pandas as pd

def transform_and_clean_data():
    print("--- Starting Data Transformation ---")
    
    master_path = "data/raw/fund_master.csv"
    history_path = "data/raw/nav_history.csv"
    processed_dir = "data/processed"
    
    os.makedirs(processed_dir, exist_ok=True)
    
    if not os.path.exists(master_path) or not os.path.exists(history_path):
        print("Error: Raw files missing!")
        return
        
    df_master = pd.read_csv(master_path)
    df_history = pd.read_csv(history_path)
    
    print(f"Original Master Rows: {len(df_master)}")
    print(f"Original History Rows: {len(df_history)}")
    
    df_master = df_master.drop_duplicates()
    df_history = df_history.drop_duplicates()
    
    df_master = df_master.dropna(subset=['scheme_code'])
    df_history = df_history.dropna(subset=['scheme_code', 'nav'])
    
    if 'date' in df_history.columns:
        df_history['date'] = pd.to_datetime(df_history['date'], errors='coerce')
        df_history = df_history.dropna(subset=['date'])
        
    print(f"Cleaned Master Rows: {len(df_master)}")
    print(f"Cleaned History Rows: {len(df_history)}")
    
    df_master.to_csv(os.path.join(processed_dir, "cleaned_fund_master.csv"), index=False)
    df_history.to_csv(os.path.join(processed_dir, "cleaned_nav_history.csv"), index=False)
    
    print("Success: Cleaned files saved in data/processed/ folder!")

if __name__ == "__main__":
    transform_and_clean_data() 