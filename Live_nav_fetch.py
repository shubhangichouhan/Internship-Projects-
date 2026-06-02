import sqlite3
import requests
from fastapi import FastAPI, HTTPException

app = FastAPI()

DB_PATH = "sql/mutual_funds.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
def home():
    return {"message": "Mutual Fund API is running successfully!"}

@app.get("/funds")
def get_all_funds():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fund_master LIMIT 10")
    funds = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {"total_funds_displayed": len(funds), "funds": funds}

@app.get("/live-nav/{scheme_code}")
def get_live_nav(scheme_code: int):
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Failed to fetch data from live API")
        
    data = response.json()
    
    if not data.get("data"):
        raise HTTPException(status_code=404, detail="Scheme code not found in live data")
        
    latest_nav_data = data["data"][0]
    meta_data = data.get("meta", {})
    
    return {
        "scheme_code": scheme_code,
        "scheme_name": meta_data.get("scheme_name"),
        "fund_house": meta_data.get("fund_house"),
        "live_date": latest_nav_data.get("date"),
        "live_nav": float(latest_nav_data.get("nav"))
    } 