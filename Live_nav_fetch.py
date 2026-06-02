import os
import requests
import pandas as pd

RAW_DIR = "data/raw"

def fetch_nav(code, name):
    url = f"https://api.mfapi.in/mf/{code}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json().get('data', [])
            if data:
                df = pd.DataFrame(data)
                df['scheme_code'] = code
                df['scheme_name'] = name
                df.to_csv(os.path.join(RAW_DIR, f"nav_{code}.csv"), index=False)
                print(f"Fetched live NAV for {name}")
    except:
        pass

if __name__ == "__main__":
    fetch_nav("125497", "HDFC Top 100 Direct")
    schemes = {
        "119551": "SBI Bluechip",
        "120503": "ICICI Bluechip",
        "118632": "Nippon Large Cap",
        "119092": "Axis Bluechip",
        "120841": "Kotak Bluechip"
    }
    for code, name in schemes.items():
        fetch_nav(code, name) 