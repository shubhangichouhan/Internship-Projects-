import os
import sqlite3
import pandas as pd

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "sql", "bluestock_mf.db")
processed_dir = os.path.join(base_dir, "data", "processed")

conn = sqlite3.connect(db_path)

try:
    df_fund = pd.read_csv(os.path.join(processed_dir, "cleaned_01_fund_master.csv"))
    df_fund.columns = [c.lower().strip() for c in df_fund.columns]
    df_fund = df_fund[['amfi_code', 'scheme_name', 'category', 'fund_house']]
    df_fund = df_fund.drop_duplicates(subset=['amfi_code'])
    df_fund.to_sql('dim_fund', conn, if_exists='append', index=False, method=lambda t, c, k, d: c.executemany(f"INSERT OR IGNORE INTO {t.name} ({', '.join(k)}) VALUES ({', '.join(['?']*len(k))})", d))

    df_nav = pd.read_csv(os.path.join(processed_dir, "cleaned_02_nav_history.csv"))
    df_nav.columns = [c.lower().strip() for c in df_nav.columns]
    
    if 'date' in df_nav.columns:
        df_nav = df_nav.rename(columns={'date': 'date_id'})
    
    if 'date_id' in df_nav.columns:
        df_date = pd.DataFrame({'date_id': df_nav['date_id'].unique()})
        df_date['date_dt'] = pd.to_datetime(df_date['date_id'])
        df_date['year'] = df_date['date_dt'].dt.year
        df_date['month'] = df_date['date_dt'].dt.month
        df_date['day'] = df_date['date_dt'].dt.day
        df_date['quarter'] = df_date['date_dt'].dt.quarter
        df_date = df_date.drop(columns=['date_dt'])
        df_date = df_date.drop_duplicates(subset=['date_id'])
        df_date.to_sql('dim_date', conn, if_exists='append', index=False, method=lambda t, c, k, d: c.executemany(f"INSERT OR IGNORE INTO {t.name} ({', '.join(k)}) VALUES ({', '.join(['?']*len(k))})", d))

    if 'nav' in df_nav.columns and 'amfi_code' in df_nav.columns and 'date_id' in df_nav.columns:
        df_nav = df_nav.drop_duplicates(subset=['date_id', 'amfi_code'])
        df_nav[['date_id', 'amfi_code', 'nav']].to_sql('fact_nav', conn, if_exists='append', index=False, method=lambda t, c, k, d: c.executemany(f"INSERT OR IGNORE INTO {t.name} ({', '.join(k)}) VALUES ({', '.join(['?']*len(k))})", d))

    df_trans = pd.read_csv(os.path.join(processed_dir, "cleaned_08_investor_transactions.csv"))
    df_trans.columns = [c.lower().strip() for c in df_trans.columns]
    df_trans = df_trans.rename(columns={
        'transaction_date': 'date_id',
        'amount_inr': 'amount'
    })
    df_trans = df_trans[['investor_id', 'amfi_code', 'transaction_type', 'amount', 'date_id']]
    df_trans.to_sql('fact_transactions', conn, if_exists='append', index=False, method=lambda t, c, k, d: c.executemany(f"INSERT OR IGNORE INTO {t.name} ({', '.join(k)}) VALUES ({', '.join(['?']*len(k))})", d))

    df_perf = pd.read_csv(os.path.join(processed_dir, "cleaned_07_scheme_performance.csv"))
    df_perf.columns = [c.lower().strip() for c in df_perf.columns]
    df_perf = df_perf.rename(columns={
        'return_1yr_pct': 'return_1y',
        'return_3yr_pct': 'return_3y',
        'return_5yr_pct': 'return_5y',
        'expense_ratio_pct': 'expense_ratio'
    })
    df_perf = df_perf[['amfi_code', 'return_1y', 'return_3y', 'return_5y', 'expense_ratio']]
    df_perf = df_perf.drop_duplicates(subset=['amfi_code'])
    df_perf.to_sql('fact_performance', conn, if_exists='append', index=False, method=lambda t, c, k, d: c.executemany(f"INSERT OR IGNORE INTO {t.name} ({', '.join(k)}) VALUES ({', '.join(['?']*len(k))})", d))

    df_aum = pd.read_csv(os.path.join(processed_dir, "cleaned_03_aum_by_fund_house.csv"))
    df_aum.columns = [c.lower().strip() for c in df_aum.columns]
    
    if 'date' in df_aum.columns:
        df_aum = df_aum.rename(columns={'date': 'date_id'})
        
    for col in df_aum.columns:
        if 'aum' in col:
            df_aum = df_aum.rename(columns={col: 'aum_amount'})
            break

    df_aum = df_aum[['fund_house', 'aum_amount', 'date_id']]
    df_aum.to_sql('fact_aum', conn, if_exists='append', index=False, method=lambda t, c, k, d: c.executemany(f"INSERT OR IGNORE INTO {t.name} ({', '.join(k)}) VALUES ({', '.join(['?']*len(k))})", d))

    print("Success")

except sqlite3.Error as sqlite_error:
    print(f"SQL Error: {sqlite_error}")
except Exception as e:
    import traceback
    print(f"Python Error: {traceback.format_exc()}")
finally:
    conn.close() 