import pandas as pd
import numpy as np

print("Loading data...")
df_nav = pd.read_csv('../data/processed/cleaned_02_nav_history.csv')

risk_metrics = df_nav.groupby('amfi_code').apply(lambda x: x['returns'].std())
risk_metrics = pd.DataFrame(risk_metrics, columns=['VaR_95']) 

def get_recommendations(risk_level):
    if risk_level == 'High':
        return risk_metrics.nlargest(3, 'VaR_95')
    else:
        return risk_metrics.nsmallest(3, 'VaR_95')

print("\n--- RECOMMENDED FUNDS ---")
print(get_recommendations('High'))
recommendation = get_recommendations('High') 
print(recommendation)