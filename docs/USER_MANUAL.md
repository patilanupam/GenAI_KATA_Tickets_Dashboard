# User Manual - Support Operations Reporting Solution

## For: Business Users & Support Teams
## Version: 1.0 | Date: 2025-12-19

---

## Table of Contents
1. [Introduction](#introduction)
2. [System Requirements](#system-requirements)
3. [Installation Guide](#installation-guide)
4. [How to Run the Solution](#how-to-run-the-solution)
5. [Understanding the Outputs](#understanding-the-outputs)
6. [Creating Dashboards in Excel](#creating-dashboards-in-excel)
7. [Troubleshooting](#troubleshooting)
8. [FAQ](#faq)

---

## Introduction

This solution automatically processes support ticket data from Hub A (Bangalore) and Hub B (Krakow), calculates performance KPIs, and generates dashboard-ready reports for leadership.

**What it does:**
- Reads ticket and effort data from CSV files
- Cleans and standardizes the data
- Calculates key performance metrics
- Generates reports ready for Excel or Power BI

**What you need:**
- Your ticket data in CSV format
- Python 3.x installed
- 5 minutes to run the script

---

## System Requirements

### Minimum Requirements
- **Operating System:** Windows 10/11, macOS 10.14+, or Linux
- **Python Version:** 3.8 or newer
- **Disk Space:** 50 MB
- **RAM:** 2 GB minimum

### Software Requirements
- Python 3.x
- pandas library
- Excel or Power BI (for viewing outputs)

---

## Installation Guide

### Step 1: Check if Python is Installed

**Windows:**
```cmd
python --version
```

**Mac/Linux:**
```bash
python3 --version
```

**Expected output:** `Python 3.8.x` or newer

If Python is not installed, download from: https://www.python.org/downloads/

### Step 2: Install Required Libraries

Open terminal/command prompt and run:

```bash
pip install pandas
```

**Expected output:**
```
Successfully installed pandas-2.x.x numpy-1.x.x ...
```

### Step 3: Verify Installation

```bash
python -c "import pandas; print('pandas version:', pandas.__version__)"
```

**Expected output:**
```
pandas version: 2.x.x
```

---

## How to Run the Solution

### Step 1: Prepare Your Files

Make sure you have these files in the same folder:
- `process_tickets.py` (the main script)
- `tickets 1.csv` (your ticket data)
- `effort 1.csv` (your agent effort data)

### Step 2: Run the Script

**Windows:**
```cmd
cd C:\Users\YourName\Documents\KATA_Tickets_Dashboard
python process_tickets.py
```

**Mac/Linux:**
```bash
cd /path/to/KATA_Tickets_Dashboard
python3 process_tickets.py
```

### Step 3: Watch the Progress

You'll see output like this:

```
======================================================================
SUPPORT OPERATIONS PERFORMANCE REPORTING
======================================================================

[1/5] Loading data...
  ✓ Loaded 100 tickets from tickets 1.csv
  ✓ Loaded 21 effort records from effort 1.csv

[2/5] Cleaning and standardizing data...
  ✓ Parsed datetime fields
  ✓ Extracted year-month
  ✓ Cleaned CSAT scores

[3/5] Enriching data with calculated fields...
  ✓ Calculated resolution time
  ✓ Determined SLA compliance
  ✓ Flagged backlog tickets
  ✓ Categorized CSAT scores
  ✓ Saved cleaned data to outputs/tickets_master.csv

[4/5] Computing KPIs...
  ✓ Saved KPI summary to outputs/kpi_monthly_summary.csv

[5/5] Computing agent performance metrics...
  ✓ Saved agent performance to outputs/agent_performance.csv

======================================================================
PROCESSING COMPLETE!
======================================================================
```

### Step 4: Find Your Outputs

A new folder called `outputs` will be created with 3 CSV files inside.

---

## Understanding the Outputs

### Output 1: tickets_master.csv

**Purpose:** Clean, standardized ticket data with calculated fields

**Key Columns:**
- `ticket_id`: Unique ticket identifier
- `hub`: A (Bangalore) or B (Krakow)
- `function`: IT, HR, or Finance
- `created_datetime`: When ticket was created
- `resolved_datetime`: When ticket was resolved
- `resolution_time_hours`: How long it took (in hours)
- `sla_met`: TRUE if met SLA, FALSE if missed
- `csat_score`: Customer satisfaction (1-5)
- `is_backlog`: TRUE if still open/in progress

**Use this file for:**
- Detailed ticket analysis
- Finding specific tickets
- Understanding individual cases

### Output 2: kpi_monthly_summary.csv

**Purpose:** Pre-calculated KPIs grouped by month, hub, and function

**Key Columns:**
- `year_month`: Month of the data (e.g., 2025-10)
- `hub`: A or B
- `function`: IT, HR, or Finance
- `total_tickets`: Total tickets created
- `sla_compliance_pct`: % of tickets that met SLA
- `avg_resolution_time_hours`: Average time to resolve
- `backlog_count`: Open/in progress tickets
- `csat_avg_score`: Average satisfaction score
- `reopen_rate_pct`: % of tickets reopened

**Use this file for:**
- Leadership dashboards
- Monthly reports
- Hub comparisons
- Trend analysis

### Output 3: agent_performance.csv

**Purpose:** Agent-level workload and efficiency metrics

**Key Columns:**
- `agent_id`: Agent identifier (e.g., AG-001)
- `hub`: A or B
- `function`: IT, HR, or Finance
- `month`: Month of data
- `tickets_handled`: Number of tickets worked on
- `total_working_hours`: Total hours agent worked
- `ticket_work_hours`: Hours spent on tickets
- `utilization_pct`: % of time spent on tickets

**Use this file for:**
- Agent performance reviews
- Workload balancing
- Capacity planning

---

## Creating Dashboards in Excel

### Quick Start Dashboard (10 minutes)

**Step 1: Open the KPI Summary**
1. Open Excel
2. File → Open → Select `outputs/kpi_monthly_summary.csv`

**Step 2: Create a Pivot Table**
1. Click anywhere in the data
2. Insert → PivotTable
3. Choose "New Worksheet"
4. Click OK

**Step 3: Build Your First Chart**

**Ticket Volume Over Time:**
- Drag `year_month` to Rows
- Drag `hub` to Columns
- Drag `total_tickets` to Values
- Insert → Chart → Line Chart

**SLA Compliance Comparison:**
- Drag `hub` to Rows
- Drag `sla_compliance_pct` to Values
- Insert → Chart → Column Chart

**CSAT Trends:**
- Drag `year_month` to Rows
- Drag `csat_avg_score` to Values
- Drag `hub` to Legend
- Insert → Chart → Line Chart

### Dashboard Template

Create a dashboard with these 5 key visuals:

1. **Top Section:** Key metrics cards
   - Total tickets
   - Average SLA compliance
   - Average CSAT
   - Current backlog

2. **Middle Section:** Trend charts
   - Ticket volume over time (line chart)
   - SLA compliance trend (line chart)

3. **Bottom Section:** Comparisons
   - Hub A vs Hub B table
   - Top categories (bar chart)

---

## Troubleshooting

### Problem: "python: command not found"

**Solution:**
- Python is not installed or not in PATH
- Try `python3` instead of `python`
- Reinstall Python and check "Add to PATH" during installation

### Problem: "No module named 'pandas'"

**Solution:**
```bash
pip install pandas
```

If that doesn't work, try:
```bash
pip3 install pandas
```

### Problem: "FileNotFoundError: tickets 1.csv"

**Solution:**
- Make sure you're in the correct directory
- Check that the CSV files exist
- Verify file names match exactly (including spaces)

**Check your location:**
```bash
# Windows
cd
dir

# Mac/Linux
pwd
ls
```

### Problem: Script runs but no outputs folder created

**Solution:**
- Check for error messages in the console
- Verify you have write permissions in the folder
- Try running as administrator (Windows) or with sudo (Mac/Linux)

### Problem: "PermissionError" when creating files

**Solution:**
- Close Excel if any output files are open
- Run the script with administrator privileges
- Check folder permissions

### Problem: Numbers look wrong in Excel

**Solution:**
- Excel might interpret dates or numbers incorrectly
- Use "Text Import Wizard" when opening CSV
- Or change column format to "Number" or "General"

### Problem: CSAT scores showing as 0

**Solution:**
- This is normal - tickets without CSAT responses show as 0
- Use the `csat_avg_score` column which excludes zero values
- Check `csat_responses` column to see how many valid responses

---

## FAQ

**Q: How often should I run this script?**
A: Run it weekly or monthly, depending on reporting needs. You can schedule it to run automatically.

**Q: Can I use different CSV file names?**
A: Yes, edit the top of `process_tickets.py` and change `INPUT_TICKETS` and `INPUT_EFFORT` variables.

**Q: What if my CSV has different column names?**
A: You'll need to modify the script to map your column names to the expected ones. Contact your data engineer for help.

**Q: Can I add more hubs?**
A: Yes, the script handles any number of hubs. Just include them in your CSV files.

**Q: What if I don't have effort data?**
A: The script will still work. You just won't get the `agent_performance.csv` output.

**Q: Can I run this on real-time data?**
A: This solution is designed for batch processing. For real-time, you'd need a database and streaming solution.

**Q: How do I share the dashboard with leadership?**
A: Save your Excel file with charts and email it, or publish to SharePoint/Power BI.

**Q: What if I find a bug?**
A: Document the issue with screenshots and contact your data engineering team.

**Q: Can I customize the KPIs?**
A: Yes! Modify the KPI calculation section (Step 4) in the Python script. Add your own metrics.

**Q: Is this production-ready?**
A: This is a prototype/demo solution. For production, you'd add error handling, logging, testing, and automation.

---

## Need Help?

### Quick Support

**Technical Issues:**
→ Contact: Data Engineering Team

**Business Questions:**
→ Contact: Analytics Team

**Dashboard Design:**
→ Contact: Business Intelligence Team

### Resources

- Python Documentation: https://docs.python.org/3/
- Pandas User Guide: https://pandas.pydata.org/docs/user_guide/
- Excel Training: https://support.microsoft.com/excel

---

## Appendix: Sample Commands

### Running on Schedule (Advanced)

**Windows (Task Scheduler):**
Create a batch file `run_report.bat`:
```batch
cd C:\path\to\KATA_Tickets_Dashboard
python process_tickets.py
```

**Mac/Linux (Cron):**
```bash
0 9 * * 1 cd /path/to/KATA_Tickets_Dashboard && python3 process_tickets.py
```
(Runs every Monday at 9 AM)

### Processing Multiple Months

If you have multiple CSV files:
```bash
python process_tickets.py
# Rename outputs folder to outputs_jan
mkdir outputs_jan
move outputs/* outputs_jan/

# Update CSV files and run again
python process_tickets.py
```

---

## Change Log

**Version 1.0 (2025-12-19)**
- Initial release
- Basic ticket processing
- KPI calculations
- Agent performance metrics

---

*For questions or feedback, contact your project team lead.*
