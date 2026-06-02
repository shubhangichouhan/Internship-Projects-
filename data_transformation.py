import os
import pandas as pd

RAW_DIR = os.path.join("data", "raw")
PROCESSED_DIR = os.path.join("data", "processed")

def clean_nav_data(df):
    df['date'] = pd.to_datetime(df['date'], format='mixed', dayfirst=True)
    df = df.sort_values('date')
    
    full_range = pd.date_range(start=df['date'].min(), end=df['date'].max(), freq='D')
    df = df.set_index('date').reindex(full_range)
    df['nav'] = df['nav'].ffill()
    
    df = df.reset_index().rename(columns={'index': 'date'})
    return df

def transform_all_data():
    if not os.path.exists(RAW_DIR):
        return

    os.makedirs(PROCESSED_DIR, exist_ok=True)
    
    for file in os.listdir(RAW_DIR):
        if file.startswith("nav_") and file.endswith(".csv"):
            df = pd.read_csv(os.path.join(RAW_DIR, file))
            cleaned_df = clean_nav_data(df)
            cleaned_df.to_csv(os.path.join(PROCESSED_DIR, f"cleaned_{file}"), index=False)
            
    print("Data transformation completed successfully.")

if __name__ == "__main__":
    transform_all_data() 