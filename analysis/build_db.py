import pandas as pd
import sqlite3

incidents = pd.read_csv("../data/cleaned_incidents.csv")
incidents["made_sla"] = (incidents["made_sla"].astype(str).str.strip().str.lower() == "true").astype(int)

conn = sqlite3.connect("../data/incidents.db")
incidents.to_sql("incidents", conn, if_exists="replace", index=False)
conn.close()

print("Database created.")
