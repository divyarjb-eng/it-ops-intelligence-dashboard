# Enterprise IT Operations Intelligence Dashboard

An ETL and analytics pipeline examining IT incident management data to identify SLA compliance risk, build a validated risk-scoring model, and generate management-level recommendations for an IT operations team.

## Business Problem

An enterprise IT department needs to know whether it's meeting SLA targets, which incidents carry the highest operational risk, and where to focus process improvement to reduce delays on its most critical issues.

## Dataset

[Incident Management Process Enriched Event Log](https://archive.ics.uci.edu/dataset/498/incident+management+process+enriched+event+log), UCI Machine Learning Repository (CC BY 4.0). Real, anonymized incident data (141,712 log events / 24,918 incidents) from a ServiceNow instance at an IT company. This dataset is not my own; used here for educational/portfolio analysis only. To reproduce, download from the link above and place `incident_event_log.csv` in the `data/` folder.

## Tools

Python (pandas, matplotlib), SQL, SQLite, Streamlit, Git/GitHub.
## Key Findings

1. **SLA compliance inverts with priority.** Critical incidents meet their SLA only 33.5% of the time, vs. 97.4% for Low priority — the most urgent incidents are the least reliably handled.
2. **Critical incidents also take the longest to resolve in absolute terms** (median 75.9 hours vs. 4.8 hours for Low priority) — ruling out "too-tight SLA window" as the explanation; this is a genuine resolution-speed problem.
3. **A custom risk score built independently from `impact` x `urgency` (via SQL CASE) reproduces the system's own priority classification almost exactly** (266 "Severe Risk" incidents at 33.5% SLA vs. 266 "1 - Critical" incidents at 33.5% SLA) — validating both the scoring approach and the priority field.
4. **Operational risk is concentrated, not evenly spread.** One incident category accounts for more Critical-priority incidents than the next two categories combined.

## Recommendations

1. Investigate root causes of Critical-incident delays specifically — reassignment volume only partially explains the gap, pointing to deeper process or staffing issues on complex incidents.
2. Prioritize process review for the top Critical-driving category, which generates a disproportionate share of high-risk volume.
3. Use the validated impact x urgency risk score as an early-warning flag to route high-risk incidents to senior responders before SLA breach.
## Project Structure
it-ops-intelligence-dashboard/
├── analysis/          # ETL, cleaning, KPI analysis, chart generation, SQLite build scripts
├── data/               # not included — see Dataset section to reproduce
├── app.py              # Streamlit dashboard
├── requirements.txt
└── README.md
## How to Run

1. Clone this repo and cd into it.
2. Install dependencies: pip3 install -r requirements.txt
3. Download the dataset (see Dataset section) into data/incident_event_log.csv
4. From analysis/, run python3 clean.py to generate the cleaned, collapsed incident dataset, then python3 build_db.py to build the SQLite database.
5. From the project root, run streamlit run app.py to launch the dashboard.

## Limitations & Future Work

- The cmdb_ci (configuration item / asset) field is 99.7% missing in the source data, limiting true asset-level analysis; category/subcategory were used as a practical substitute.
- Categories and assignment groups are anonymized to generic labels (e.g., "Category 46"), so risk concentration can be located but not descriptively explained without additional context.
- Reassignment count only partially explains the Critical-incident delay gap; a future version could incorporate additional fields (e.g., number of unique responders, escalation chains) to isolate the root cause further.
