import os
import sqlite3
import requests
import pandas as pd
from datetime import datetime

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "sql", "bluestock_mf.db")

def fetch_latest_nav(amfi_code):
    url = f"https://api.mfapi.in/mf/{amfi_code}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and len(data['data']) > 0:
                latest_entry = data['data'][0]
                raw_date = latest_entry['date']
                date_obj = datetime.strptime(raw_date, "%d-%m-%Y")
                
                return {
                    'date_id': raw_date,
                    'amfi_code': int(amfi_code),
                    'nav': float(latest_entry['nav'])
                }
    except Exception:
        pass
    return None

def main():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("Fetching active funds from database...")
    try:
        cursor.execute("SELECT amfi_code FROM dim_fund")
        funds = cursor.fetchall()
        
        if not funds:
            print("No funds found in dim_fund table.")
            return
            
        new_nav_data = []
        for (amfi_code,) in funds[:5]: 
            print(f"Fetching live NAV for AMFI Code: {amfi_code}...")
            nav_info = fetch_latest_nav(amfi_code)
            if nav_info:
                new_nav_data.append(nav_info)
        
        if new_nav_data:
            df_new_nav = pd.DataFrame(new_nav_data)
            df_new_nav.to_sql('fact_nav', conn, if_exists='append', index=False, 
                              method=lambda t, c, k, d: c.executemany(
                                  f"INSERT OR IGNORE INTO {t.name} ({', '.join(k)}) VALUES ({', '.join(['?']*len(k))})", d
                              ))
            print(f"Successfully automated & loaded {len(new_nav_data)} new NAV records!")
        else:
            print("No new data fetched.")
            
    except Exception as e:
        print(f"Pipeline Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main() 