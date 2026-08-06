import pandas as pd

# Load raw event log
df = pd.read_csv("../data/incident_event_log.csv", na_values="?", low_memory=False)

# Collapse to one row per incident (final state)
df_sorted = df.sort_values(["number", "sys_updated_at"])
incidents = df_sorted.groupby("number").last().reset_index()

# Drop columns that are almost entirely empty or not useful for analysis
columns_to_drop = [
    "cmdb_ci", "vendor", "caused_by", "rfc", "problem_id",
    "sys_created_by", "sys_updated_by", "opened_by", "notify",
    "u_priority_confirmation", "knowledge"
]
incidents = incidents.drop(columns=columns_to_drop)

# Convert date columns to real datetimes (day-first format, e.g. 29/2/2016)
date_columns = ["opened_at", "sys_created_at", "sys_updated_at", "resolved_at", "closed_at"]
for col in date_columns:
    incidents[col] = pd.to_datetime(incidents[col], dayfirst=True, errors="coerce")

# Calculate resolution time in hours
incidents["resolution_hours"] = (incidents["resolved_at"] - incidents["opened_at"]).dt.total_seconds() / 3600

# Validate
print(incidents.shape)
print(incidents.isnull().sum())
print(incidents["resolution_hours"].describe())

# Save cleaned data
incidents.to_csv("../data/cleaned_incidents.csv", index=False)
print("Saved cleaned_incidents.csv")
