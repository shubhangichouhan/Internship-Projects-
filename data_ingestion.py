import os
import glob
import pandas as pd

def load_and_inspect_datasets():
    print("--- Loading and Inspecting CSV Datasets ---")
    
    csv_files = glob.glob("data/raw/*.csv")
    
    for file in csv_files[:10]:
        print("\n========================================")
        print(f"Dataset: {file}")
        print("========================================")
        
        try:
            df = pd.read_csv(file)
            print(f"Shape: {df.shape}")
            print("\nData Types:")
            print(df.dtypes)
            print("\nFirst 3 Rows:")
            print(df.head(3))
            
            missing_values = df.isnull().sum().sum()
            if missing_values > 0:
                print(f"Note: Found {missing_values} missing values in this file.")
                
        except Exception as e:
            print(f"Could not read {file}: {e}")

def explore_and_validate_fund_master():
    print("\n--- Exploring Fund Master ---")
    master_path = "data/raw/fund_master.csv" 
    history_path = "data/raw/nav_history.csv"
    
    if not os.path.exists(master_path) or not os.path.exists(history_path):
        print("Error: Required master or history file missing in data/raw/")
        return
        
    df_master = pd.read_csv(master_path)
    df_history = pd.read_csv(history_path)
    
    if 'fund_house' in df_master.columns:
        print("\nUnique Fund Houses:")
        print(df_master['fund_house'].unique())
        
    if 'category' in df_master.columns:
        print("\nUnique Categories:")
        print(df_master['category'].unique())
        
    if 'sub_category' in df_master.columns:
        print("\nUnique Sub-Categories:")
        print(df_master['sub_category'].unique())
        
    if 'risk_grade' in df_master.columns:
        print("\nUnique Risk Grades:")
        print(df_master['risk_grade'].unique())
            
    master_codes = set(df_master['scheme_code'].unique())
    history_codes = set(df_history['scheme_code'].unique())
    
    missing_in_history = master_codes - history_codes
    
    print("\n--- Data Quality Summary ---")
    print(f"Total unique AMFI codes in Master: {len(master_codes)}")
    print(f"Total unique AMFI codes in NAV History: {len(history_codes)}")
    
    if len(missing_in_history) == 0:
        print("Validation Success: Every code in fund_master exists in nav_history.")
    else:
        print(f"Validation Alert: {len(missing_in_history)} codes from fund_master are missing in nav_history.")

if __name__ == "__main__":
    load_and_inspect_datasets()
    explore_and_validate_fund_master()