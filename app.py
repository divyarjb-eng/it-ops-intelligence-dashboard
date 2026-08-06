import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

incidents = pd.read_csv("data/cleaned_incidents.csv")
incidents["made_sla"] = (incidents["made_sla"].astype(str).str.strip().str.lower() == "true").astype(int)
incidents["opened_at"] = pd.to_datetime(incidents["opened_at"])

st.title("Enterprise IT Operations Intelligence Dashboard")

st.sidebar.header("Filters")
priority_options = ["1 - Critical", "2 - High", "3 - Moderate", "4 - Low"]
selected_priorities = st.sidebar.multiselect(
    "Priority",
    options=priority_options,
    default=priority_options
)

filtered = incidents[incidents["priority"].isin(selected_priorities)].copy()

st.subheader("Key Metrics")
sla_rate = filtered["made_sla"].mean() * 100
total_incidents = len(filtered)
median_resolution = filtered["resolution_hours"].median()

col1, col2, col3 = st.columns(3)
col1.metric("SLA Compliance Rate", f"{sla_rate:.1f}%")
col2.metric("Total Incidents", f"{total_incidents:,}")
col3.metric("Median Resolution Time", f"{median_resolution:.1f} hrs")

st.subheader("SLA Compliance Rate by Priority")
sla_by_priority = filtered.groupby("priority")["made_sla"].mean() * 100
sla_by_priority = sla_by_priority.reindex(priority_options).dropna()
fig1, ax1 = plt.subplots()
ax1.bar(sla_by_priority.index, sla_by_priority.values, color="crimson")
ax1.set_ylabel("SLA Compliance Rate (%)")
st.pyplot(fig1)

st.subheader("Median Resolution Time by Priority")
resolution_by_priority = filtered.groupby("priority")["resolution_hours"].median()
resolution_by_priority = resolution_by_priority.reindex(priority_options).dropna()
fig2, ax2 = plt.subplots()
ax2.bar(resolution_by_priority.index, resolution_by_priority.values, color="darkorange")
ax2.set_ylabel("Resolution Time (hours)")
st.pyplot(fig2)

st.subheader("SLA Compliance Over Time")
filtered["open_month"] = filtered["opened_at"].dt.to_period("M").astype(str)
sla_by_month = filtered.groupby("open_month")["made_sla"].mean() * 100
fig3, ax3 = plt.subplots(figsize=(10, 4))
ax3.plot(sla_by_month.index, sla_by_month.values, marker="o", color="darkred")
ax3.set_ylabel("SLA Compliance Rate (%)")
plt.setp(ax3.get_xticklabels(), rotation=45, ha="right")
st.pyplot(fig3)

st.subheader("Risk Tier Breakdown")
def risk_tier(row):
    if row["impact"] == "1 - High" and row["urgency"] == "1 - High":
        return "Severe Risk"
    elif row["impact"] == "1 - High" or row["urgency"] == "1 - High":
        return "Elevated Risk"
    else:
        return "Standard Risk"

filtered["risk_tier"] = filtered.apply(risk_tier, axis=1)
risk_summary = filtered.groupby("risk_tier").agg(
    incident_count=("number", "count"),
    sla_rate_pct=("made_sla", "mean")
)
risk_summary["sla_rate_pct"] = risk_summary["sla_rate_pct"] * 100
st.dataframe(risk_summary)

st.subheader("Top Assignment Groups by Volume")
group_summary = filtered.groupby("assignment_group").agg(
    incident_count=("number", "count"),
    sla_rate_pct=("made_sla", "mean")
).sort_values("incident_count", ascending=False).head(10)
group_summary["sla_rate_pct"] = group_summary["sla_rate_pct"] * 100
st.dataframe(group_summary)

st.subheader("Key Business Insights")
st.markdown("""
- **SLA compliance inverts with priority.** Critical incidents comply only 33.5% of the time vs. 97.4% for Low priority — the most urgent issues are the least reliably handled.
- **Critical incidents also take the longest to resolve in absolute terms** (median 75.9 hours vs. 4.8 hours for Low) — this isn't a too-tight-SLA-window problem, it's a genuine resolution-speed problem.
- **A custom risk score (impact × urgency) independently validates the system's priority field** — Severe Risk incidents match Critical priority almost exactly.
- **Risk is concentrated, not evenly spread.** One category accounts for more Critical incidents than the next two categories combined.
""")

st.subheader("Recommendations")
st.markdown("""
1. Investigate root causes of Critical-incident delays specifically — reassignment volume only partially explains the gap.
2. Prioritize process review for the top Critical-driving category, which generates a disproportionate share of high-risk volume.
3. Use the validated impact × urgency risk score as an early-warning flag to route high-risk incidents to senior responders before SLA breach.
""")
