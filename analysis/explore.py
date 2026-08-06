import pandas as pd

df = pd.read_csv("../data/incident_event_log.csv", na_values="?")

print(df.shape)
print(df.columns.tolist())
print(df.head())
df_sorted = df.sort_values(["number", "sys_updated_at"])
incidents = df_sorted.groupby("number").last().reset_index()

print(incidents.shape)
print(incidents["incident_state"].value_counts())
