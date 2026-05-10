# BA Prep — Top-Tier Business Analyst Interview Engine

A high-performance, comprehensive interview simulation platform engineered specifically for Senior Business Analyst and Strategy roles at top-tier tech firms and consulting groups (Stripe, McKinsey, JPMorgan, Amazon, Google). 

This is not a basic quiz app—it is an **exhaustive 400+ question assessment engine** that simulates exact interview loops, from complex SaaS Unit Economics to DAX Query Folding limitations.

![BA Prep Interface](https://img.shields.io/badge/Status-Complete-success?style=for-the-badge)
![Tech Stack](https://img.shields.io/badge/FastAPI-Python-blue?style=for-the-badge&logo=fastapi)
![Vanilla JS](https://img.shields.io/badge/Vanilla-JS-yellow?style=for-the-badge&logo=javascript)

## 🚀 The 400+ Question Curriculum

The platform spans **72 Chapters** across **7 Core Modules**, each fully mapped to official documentation and advanced learning resources.

| Module | Focus Areas | Volume |
|--------|-------------|--------|
| 📊 **Excel Mastery** | VLOOKUP/XLOOKUP, INDEX MATCH, Dynamic Arrays, Nested IFs | 60 Qs |
| ⚡ **Power BI** | Star Schema, Query Folding, Time Intelligence, DAX Optimization | 56 Qs |
| 📈 **Tableau** | LOD Expressions, Table Calcs, Order of Operations, Dashboard Perf | 56 Qs |
| 🧠 **Business Aptitude** | Bayes Theorem, SaaS MRR Waterfalls, Fermi Market Sizing | 64 Qs |
| 🔍 **Case Studies** | M&A Synergy, GTM Strategy, A/B Testing, Competitor War Gaming | 96 Qs |
| 🎯 **Amazon LP** | Extreme tension scenarios spanning all 16 Leadership Principles | 64 Qs |
| 📉 **Data Interpretation**| Simpson's Paradox, Advanced Regressions, Funnel Drop-offs | 70 Qs |

## ✨ Key Features

* **Real-World Scenarios**: Questions sourced directly from modern fintech and banking interview patterns.
* **Smart Validation Engine**: Handles complex string parsing, ignores absolute references in formulas, and gracefully handles currency/shorthand notation (`$1.2M`, `1200k`).
* **Excel Export Integration**: One-click TSV copying for all data tables. Instantly export data to Excel/Sheets to build your own Pivot Tables and validate your answers manually.
* **Persistent Progress**: Local storage saves your active chapter, question timers, drafts, and solved state automatically.
* **Reference Linked**: Every single chapter features a `Notes ↗` button linking directly to official Microsoft, Tableau, or Harvard Business Review documentation.

## 🛠️ Local Setup

The app runs on an ultra-lightweight FastAPI backend with a vanilla HTML/JS Single Page Application frontend.

```bash
# Clone the repository
git clone https://github.com/hahayush/business-analyst-practice.git
cd business-analyst-practice

# Set up virtual environment
python -m venv .venv
source .venv/bin/activate  # Or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the local server
uvicorn app.main:app --reload --port 8080
```
Open `http://localhost:8080` in your browser.

## ☁️ Render Deployment

This repository is built with a `render.yaml` Blueprint specification for instant deployment.
1. Connect this repo to [Render](https://dashboard.render.com).
2. Create a new **Blueprint**.
3. Render will automatically provision the Python Web Service and launch the app.