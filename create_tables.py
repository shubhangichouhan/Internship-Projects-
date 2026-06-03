import sqlite3
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "sql", "bluestock_mf.db")
schema_path = os.path.join(base_dir, "sql", "schema.sql")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

with open(schema_path, "r") as f:
    sql_script = f.read()

try:
    cursor.executescript(sql_script)
    conn.commit()
    print("Success")
except Exception as e:
    print(e)
finally:
    conn.close() 