# BA Prep — Business Analyst Interview Preparation

Comprehensive, interview-grade preparation platform for Business Analyst roles at companies like Amazon, Stripe, Google, and McKinsey.

## Modules

| Module | Topics | Questions |
|--------|--------|-----------|
| 📊 **Excel Mastery** | VLOOKUP, INDEX MATCH, Pivot Tables, IF/COUNTIF/SUMIF, Data Cleaning | 25+ |
| ⚡ **Power BI** | Data Modeling, DAX, Time Intelligence, Visualizations | 20+ |
| 📈 **Tableau** | Calculated Fields, LOD Expressions, Table Calculations, Data Prep | 20+ |
| 🧠 **Business Aptitude** | Logical Reasoning, Quant, Data Sufficiency, Probability | 20+ |
| 🔍 **Case Studies** | Metric Drops, KPI Definition, A/B Testing, Process Optimization | 20+ |
| 🎯 **Leadership Principles** | Customer Obsession, Ownership, Dive Deep, Bias for Action | 20+ |
| 📉 **Data Interpretation** | Tables, Charts, Operational Dashboards, Financial Data | 20+ |

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080
```

Open http://localhost:8080

## Tech Stack

- **Backend:** FastAPI (Python)
- **Frontend:** Vanilla HTML/CSS/JS (SPA)
- **Design:** Dark theme, Inter font, responsive
- **Persistence:** localStorage (progress, timers)