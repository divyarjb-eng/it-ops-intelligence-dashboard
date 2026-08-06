import pandas as pd

incidents = pd.read_csv("../data/cleaned_incidents.csv")

# The SLA flag can come in as text ("true"/"false") depending on how it's read —
# force it to a real boolean so .mean() works correctly no matter what.
incidents["made_sla"] = incidents["made_sla"].astype(str).str.strip().str.lower() == "true"

# KPI 1: overall SLA compliance rate
sla_rate = incidents["made_sla"].mean() * 100
print(f"Overall SLA compliance rate: {sla_rate:.1f}%")

# KPI 2: SLA compliance by priority
sla_by_priority = incidents.groupby("priority")["made_sla"].mean() * 100
print(sla_by_priority.sort_values())
# KPI 3: median resolution time by priority (median, not mean, since we know it's skewed)
resolution_by_priority = incidents.groupby("priority")["resolution_hours"].median()
print(resolution_by_priority.sort_values())
# KPI 4: does reassignment explain the delay? Median reassignment count by priority
reassignment_by_priority = incidents.groupby("priority")["reassignment_count"].median()
print(reassignment_by_priority.sort_values())
# KPI 5: which categories generate the most Critical-priority incidents?
critical = incidents[incidents["priority"] == "1 - Critical"]
critical_by_category = critical["category"].value_counts().head(10)
print(critical_by_category)

