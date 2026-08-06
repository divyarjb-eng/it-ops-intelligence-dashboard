import pandas as pd
import matplotlib.pyplot as plt

incidents = pd.read_csv("../data/cleaned_incidents.csv")
incidents["made_sla"] = incidents["made_sla"].astype(str).str.strip().str.lower() == "true"

sla_by_priority = incidents.groupby("priority")["made_sla"].mean() * 100
sla_by_priority = sla_by_priority.reindex(["1 - Critical", "2 - High", "3 - Moderate", "4 - Low"])

plt.figure(figsize=(8, 5))
plt.bar(sla_by_priority.index, sla_by_priority.values, color="crimson")
plt.title("SLA Compliance Rate by Priority")
plt.xlabel("Priority")
plt.ylabel("SLA Compliance Rate (%)")
plt.tight_layout()
plt.savefig("sla_compliance_by_priority.png")
print("Saved chart.")

resolution_by_priority = incidents.groupby("priority")["resolution_hours"].median()
resolution_by_priority = resolution_by_priority.reindex(["1 - Critical", "2 - High", "3 - Moderate", "4 - Low"])

plt.figure(figsize=(8, 5))
plt.bar(resolution_by_priority.index, resolution_by_priority.values, color="darkorange")
plt.title("Median Resolution Time by Priority")
plt.xlabel("Priority")
plt.ylabel("Resolution Time (hours)")
plt.tight_layout()
plt.savefig("resolution_time_by_priority.png")
print("Saved chart.")
incidents["opened_at"] = pd.to_datetime(incidents["opened_at"])
incidents["open_month"] = incidents["opened_at"].dt.to_period("M").astype(str)

sla_by_month = incidents.groupby("open_month")["made_sla"].mean() * 100

plt.figure(figsize=(10, 4))
plt.plot(sla_by_month.index, sla_by_month.values, marker="o", color="darkred")
plt.title("SLA Compliance Rate Over Time")
plt.xlabel("Month Opened")
plt.ylabel("SLA Compliance Rate (%)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("sla_compliance_over_time.png")
print("Saved chart.")
