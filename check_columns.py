import os
import pandas as pd

raw_dir = os.path.join("data", "raw")
for file in os.listdir(raw_dir):
    if file.endswith('.csv'):
        df = pd.read_csv(os.path.join(raw_dir, file), nrows=1)
        print(f"{file}: {list(df.columns)}") 