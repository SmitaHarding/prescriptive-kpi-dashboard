# Prescriptive KPI & Performance Dashboard
### Autonomous Operational Governance Agent

---

## What this is

Not a dashboard. An **AI-native PMO Governance Agent** that:
- Stores 16 weeks of operational KPI data in a local database
- Automatically detects SLA breaches and week-over-week deterioration
- Uses Claude AI to explain *why* metrics dropped (cross-referencing data with operational logs)
- Prescribes 3 specific, VP-ready interventions — ready for a steering committee
![Dashboard screenshot](docs/screenshot.png)

---

## Setup (one time)

### 1. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 2. Build the database
```bash
python build_database.py
```

### 3. Set your Claude API key
```bash
# Mac / Linux
export ANTHROPIC_API_KEY="sk-ant-your-key-here"

# Windows
set ANTHROPIC_API_KEY=sk-ant-your-key-here
```
Get your key at: https://console.anthropic.com

### 4. Launch the dashboard
```bash
streamlit run app.py
```

---

## File structure

| File | Purpose |
|------|---------|
| `build_database.py` | Creates and seeds the SQLite KPI database |
| `detect_anomalies.py` | Queries data, flags breaches & deterioration |
| `ai_agent.py` | Claude AI agent — root cause + prescriptive interventions |
| `app.py` | Streamlit visual dashboard |
| `kpi_dashboard.db` | SQLite database (created by build_database.py) |

---

## KPI definitions & SLA targets

| KPI | SLA Target |
|-----|-----------|
| Payment Accuracy Rate | ≥ 97% |
| Manual Processing Hours | < 200 hrs/week |
| SLA Breach Count | 0 |
| First-Pass Resolution Rate | ≥ 95% |
| Processing Cycle Time | < 3 days |

---

## Quick overview

> *"I built an Autonomous Operational Governance Agent that connects directly to process data models. The moment an SLA breach is detected, the system cross-references quantitative KPI data with qualitative operational logs, then uses a Claude AI agent — acting as a Transformation Lead — to autonomously synthesise the root cause and draft three prescriptive mitigation strategies. This eliminates manual reporting lag and scales steering committee readiness."*
