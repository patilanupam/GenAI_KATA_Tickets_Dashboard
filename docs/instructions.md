Below is a **ready-to-use, copy-paste Markdown prompt** specifically written to **feed into Claude Code** (or any code-focused LLM).
It is structured, explicit, time-boxed, and aligned with the **KATA expectations**.
You can paste this **as-is** into Claude Code.

---

```md
# 🚀 TASK: Build a Support Operations Performance Reporting Solution (1-Hour Kata)

You are acting as a **Senior Data Engineer + Analytics Engineer**.

Your goal is to design and implement a **basic working solution** (not production-grade) for a **Support Operations Performance Reporting System**.

Follow **KISS, SOLID, and YAGNI principles**.  
Focus on **clarity, correctness, and speed**.

---

## 🧠 Business Context

A global organization (OrionEdge Corp.) runs two Shared Service support hubs:

- **Support Hub A (India – Bangalore)** using ServiceNow
- **Support Hub B (Europe – Krakow)** using Jira Service Management

Each hub exports:
- Ticket data
- Effort / workload data (optional)

These exports are stored in **Excel / CSV files** with:
- Different column names
- Different formats
- Inconsistent values

Leadership currently lacks:
- A unified view of ticket volumes
- SLA performance comparison
- Backlog trends
- CSAT insights

---

## 🎯 Objective

Build a **lightweight data processing + reporting solution** that:

1. Ingests ticket data from both hubs
2. Cleans and standardizes the data
3. Computes agreed KPIs
4. Outputs datasets ready for dashboards
5. Demonstrates a simple, clear architecture

⚠️ NOT required:
- Production deployment
- Authentication
- CI/CD
- Cloud infrastructure

---

## 🏗️ Architecture Expectations

Design a **simple architecture diagram (text-based)** covering:

- Data sources (Excel / CSV)
- Data processing layer
- KPI computation layer
- Output layer (dashboard-ready)

Example components:
- Python
- Pandas
- CSV outputs
- Optional: Streamlit or Power BI-ready datasets

---

## 📂 Input Assumptions

Assume the following files exist:

```

/data/
├── hub_a_tickets.csv
├── hub_b_tickets.csv
├── hub_a_effort.csv   (optional)
├── hub_b_effort.csv   (optional)

```

Column names may differ between hubs.

---

## 🧩 Core Data Model (You MUST standardize to this)

Tickets Table:
- ticket_id
- hub (Hub_A / Hub_B)
- function (IT / HR / Finance)
- category
- priority
- channel
- created_date
- resolved_date
- sla_met (boolean)
- csat_score
- agent_id

Effort Table (optional):
- agent_id
- hub
- month
- effort_hours

---

## 📊 KPIs to Compute

Compute KPIs **per month / hub / function**:

### Ticket Volume
- Total tickets
- Tickets by category, priority, channel

### SLA & Resolution
- SLA compliance %
- Average resolution time (hours)
- Backlog at month end
- Reopen rate %

### CSAT
- Average CSAT
- % High CSAT (>= 4)
- % Low CSAT (<= 2)

### Agent Metrics (if effort data exists)
- Tickets per agent
- Ticket work utilization %

---

## 🧮 Processing Requirements

1. Load CSV files
2. Rename columns to a common schema
3. Normalize categorical values
4. Parse dates properly
5. Merge Hub A and Hub B data
6. Compute KPIs using Pandas
7. Output:
   - `tickets_master.csv`
   - `kpi_monthly_summary.csv`

---

## 📈 Reporting Output

Prepare outputs suitable for dashboards showing:

1. Ticket volume trends by month
2. SLA comparison (Hub A vs Hub B)
3. CSAT trends
4. Top problem categories
5. Management summary (last month snapshot)

---

## 🧪 Quality Expectations

- Clean, readable Python code
- Modular functions
- Clear comments
- No over-engineering
- Minimal manual steps
- Easy to explain verbally

---

## 📦 Deliverables

1. Text-based architecture overview
2. Python code (Pandas-based) to:
   - Ingest
   - Clean
   - Standardize
   - Compute KPIs
3. Sample output schemas
4. Short explanation of how leadership would use the dashboard

---
