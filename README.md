# Support Operations Performance Reporting Solution

**OrionEdge Corp - Hub A & Hub B Unified Reporting: https://orion-tickets-dashboard.streamlit.app/**

---

## Quick Start 

This solution processes ticket data from two support hubs and generates performance dashboards for leadership.

### ReadMe:
1. **Read this README first**
2. **Run the script** to generate outputs
3. **Create dashboard** in Excel using the outputs

---

## What This Solution Does

Converts this:
```
❌ Two separate CSV files (Hub A ServiceNow + Hub B Jira)
❌ Different column names and formats
❌ No unified view for leadership
❌ Manual, time-consuming analysis
```

Into this:
```
✅ Clean, standardized ticket data
✅ Pre-calculated KPIs (SLA, CSAT, volumes)
✅ Dashboard-ready CSV files
✅ Hub comparison metrics
✅ Automated processing in seconds
```

---

## Project Structure

```
KATA_Tickets_Dashboard/
│
├── 📄 README.md                      ← You are here
├── 📄 TEAM_GUIDE.md                  ← Role assignments for 4-person team
├── 📄 ARCHITECTURE.md                ← System design and data flow
├── 📄 USER_MANUAL.md                 ← Detailed usage instructions
├── 📄 instructions.md                ← Original KATA requirements
│
├── 📊 tickets 1.csv                  ← INPUT: Ticket data (both hubs)
├── 📊 effort 1.csv                   ← INPUT: Agent effort data
│
├── 🐍 process_tickets.py             ← Main processing script
│
└── 📂 outputs/
    ├── tickets_master.csv            ← Clean ticket data with enrichments
    ├── kpi_monthly_summary.csv       ← KPIs by month/hub/function
    └── agent_performance.csv         ← Agent workload metrics
```

---

## Running the Solution

### Prerequisites
```bash
# Check Python is installed
python --version  # Should be 3.8 or newer

# Install pandas
pip install pandas
```

### Execute
```bash
# Navigate to project directory
cd C:\Users\AnupamPatil\Documents\KATA_Tickets_Dashboard

# Run the script
python process_tickets.py
```

### Expected Output
```
======================================================================
SUPPORT OPERATIONS PERFORMANCE REPORTING
======================================================================

[1/5] Loading data...
  [OK] Loaded 150 tickets from tickets 1.csv
  [OK] Loaded 21 effort records from effort 1.csv

[2/5] Cleaning and standardizing data...
  [OK] Parsed datetime fields
  [OK] Extracted year-month
  [OK] Cleaned CSAT scores

[3/5] Enriching data with calculated fields...
  [OK] Calculated resolution time
  [OK] Determined SLA compliance
  [OK] Flagged backlog tickets
  [OK] Categorized CSAT scores
  [OK] Saved cleaned data to outputs\tickets_master.csv

[4/5] Computing KPIs...
  [OK] Saved KPI summary to outputs\kpi_monthly_summary.csv

[5/5] Computing agent performance metrics...
  [OK] Saved agent performance to outputs\agent_performance.csv

======================================================================
PROCESSING COMPLETE!
======================================================================
```

---

## Output Files Explained

### 1. tickets_master.csv
**Purpose:** Clean, enriched ticket data

**Key Fields:**
- Original fields: ticket_id, hub, function, category, priority, etc.
- **Added fields:**
  - `resolution_time_hours`: Time to resolve (hours)
  - `sla_met`: TRUE if SLA target met, FALSE otherwise
  - `is_backlog`: TRUE if ticket still open/in progress
  - `year_month`: Month of creation for grouping

**Use for:** Detailed ticket analysis, filtering by specific criteria

---

### 2. kpi_monthly_summary.csv
**Purpose:** Pre-calculated KPIs grouped by month, hub, and function

**Metrics Included:**

**Volume Metrics:**
- `total_tickets`: Total tickets created
- `tickets_critical/high/medium/low`: Breakdown by priority
- `tickets_email/portal/phone/chat`: Breakdown by channel

**SLA Metrics:**
- `sla_compliance_pct`: % of tickets meeting SLA
- `avg_resolution_time_hours`: Average time to resolve
- `backlog_count`: Open + In Progress tickets

**Quality Metrics:**
- `csat_avg_score`: Average satisfaction (1-5 scale)
- `csat_high_pct`: % with score >= 4
- `csat_low_pct`: % with score <= 2
- `reopen_rate_pct`: % of tickets reopened

**Use for:** Leadership dashboards, trend analysis, hub comparison

---

### 3. agent_performance.csv
**Purpose:** Agent-level workload and efficiency

**Metrics Included:**
- `tickets_handled`: Number of tickets worked
- `total_working_hours`: Total hours available
- `ticket_work_hours`: Hours spent on tickets
- `utilization_pct`: % of time on ticket work
- `avg_hours_per_ticket`: Efficiency metric

**Use for:** Agent performance reviews, capacity planning

---

## Key Insights from Current Data

Based on the processed data (150 tickets, Oct-Dec 2025):

### Hub Performance Comparison
- **Hub A (Bangalore):** 77 tickets (51%)
- **Hub B (Krakow):** 73 tickets (49%)
- Relatively balanced distribution

### Function Breakdown
- **Finance:** Reimbursements, invoice disputes, budget access
- **IT:** Software installs, network issues, email problems
- **HR:** Policy clarifications, payroll queries, leave balance

### Channel Usage
- Mixed across Email, Portal, Phone, and Chat
- Analyze channel preference by function

### SLA Performance
- Overall compliance varies by month and hub
- Detailed comparison available in kpi_monthly_summary.csv

---

## Creating Dashboards

### Option 1: Excel (Quickest - 15 minutes)

1. Open `outputs/kpi_monthly_summary.csv` in Excel
2. Insert PivotTable
3. Create these visualizations:
   - Line chart: Ticket volume trends
   - Column chart: SLA compliance by hub
   - Line chart: CSAT trends over time
4. Add summary table comparing Hub A vs Hub B

### Option 2: Power BI (30 minutes)

1. Import all three CSV files
2. Create relationships if needed
3. Build interactive dashboard with filters
4. Publish to Power BI service for sharing

### Option 3: Streamlit (Advanced - for extra time)

Create a Python web app with interactive visualizations.

---

## Team Roles (1-Hour KATA)

### Person 1: Data Engineer
- Run and troubleshoot the Python script
- Validate outputs
- Support team with technical issues

### Person 2: Analytics Engineer
- Create Excel dashboard
- Calculate key insights
- Prepare metrics for presentation

### Person 3: Business Analyst
- Create presentation slides
- Document business value
- Prepare demo script

### Person 4: Quality Assurance
- Test calculations manually
- Create user manual
- Document edge cases

**See TEAM_GUIDE.md for detailed checklists and responsibilities**

---

## Timeline

| Time | Activity |
|------|----------|
| 0-15 min | Setup, read docs, understand data |
| 15-35 min | Run script, create dashboard, build presentation |
| 35-50 min | Refine outputs, test, finalize |
| 50-60 min | Final review, practice presentation |

---

## Success Criteria

Your solution is complete when:
- ✅ Python script runs without errors
- ✅ All 3 output CSV files generated
- ✅ KPI calculations verified (spot-check)
- ✅ Excel dashboard created with 4-5 charts
- ✅ Presentation ready (5-7 slides)
- ✅ Team can explain solution in 5 minutes

---

## Troubleshooting

### "python: command not found"
**Solution:** Install Python from python.org or try `python3` instead of `python`

### "No module named 'pandas'"
**Solution:** Run `pip install pandas`

### "FileNotFoundError"
**Solution:** Ensure you're in the correct directory and CSV files exist

### Script runs but no outputs
**Solution:** Check for error messages, verify write permissions

**See USER_MANUAL.md for comprehensive troubleshooting guide**

---

## Architecture Overview

```
CSV Files (Input)
      ↓
Python + Pandas (Processing)
      ↓
Clean Data + KPIs (Output)
      ↓
Excel/Power BI (Dashboard)
      ↓
Leadership Reports
```

**See ARCHITECTURE.md for detailed system design**

---

## Sample Business Questions Answered

This solution enables leadership to answer:

1. **Volume:** How many tickets are we handling per month?
2. **Comparison:** Which hub performs better on SLA?
3. **Trends:** Are CSAT scores improving or declining?
4. **Categories:** What are the most common problem types?
5. **Efficiency:** Are agents over or under-utilized?
6. **Backlog:** Do we have a growing backlog problem?

---

## Key Technologies

| Technology | Purpose | Why? |
|------------|---------|------|
| Python 3.x | Processing engine | Easy to learn, powerful |
| Pandas | Data manipulation | Industry standard |
| CSV | Data format | Simple, universal |
| Excel/Power BI | Visualization | Familiar to business users |

---

## Design Principles

- **KISS:** Keep It Simple - no complex infrastructure
- **YAGNI:** Only build what's needed for KPIs
- **SOLID:** Modular, readable code
- **Beginner-Friendly:** Extensive comments, clear naming

---

## Next Steps (After KATA)

### Short Term (Week 1-2)
1. Schedule weekly script runs
2. Distribute dashboard to leadership
3. Gather feedback on metrics

### Medium Term (Month 1-3)
1. Add more data sources (if available)
2. Implement data quality checks
3. Create automated email reports

### Long Term (Quarter 1-2)
1. Move to database (PostgreSQL/MySQL)
2. Build real-time dashboard
3. Add predictive analytics (ML)
4. Implement alerting for SLA breaches

---

## Learning Resources

### Python & Pandas
- Official Pandas Docs: https://pandas.pydata.org/docs/
- Python DateTime: https://docs.python.org/3/library/datetime.html
- Real Python Tutorials: https://realpython.com/

### Data Analysis
- Excel Pivot Tables: https://support.microsoft.com/excel
- Power BI Learning: https://docs.microsoft.com/power-bi/

### Best Practices
- Clean Code: https://github.com/zedr/clean-code-python
- Pandas Best Practices: https://pandas.pydata.org/docs/user_guide/

---

## FAQ

**Q: Can I modify the script?**
A: Yes! It's designed to be beginner-friendly. Add your own KPIs or data cleaning steps.

**Q: What if my CSV has different columns?**
A: Edit the script to map your columns to the expected field names.

**Q: How do I schedule this to run automatically?**
A: Use Windows Task Scheduler (Windows) or cron (Mac/Linux). See USER_MANUAL.md.

**Q: Can this handle millions of tickets?**
A: For large datasets, consider using a database and Dask instead of Pandas.

**Q: Is this production-ready?**
A: This is a prototype. For production, add error handling, logging, testing, and monitoring.

---

## Credits

**Created for:** OrionEdge Corp Support Operations KATA
**Date:** December 2025
**Purpose:** 1-hour team coding challenge
**Team Size:** 4 members
**Skill Level:** Beginner-friendly

---

## Support & Feedback

**During KATA:**
- Use team chat for questions
- Check TEAM_GUIDE.md for role-specific help
- Review USER_MANUAL.md for technical issues

**After KATA:**
- Discuss lessons learned as a team
- Document improvements for next time
- Share feedback on the solution design

---

## License & Usage

This solution is created for educational purposes (KATA challenge).
Feel free to modify, extend, and use for learning.

---

## Summary

You now have a **complete, working solution** that:
- ✅ Processes ticket data from two hubs
- ✅ Calculates key performance metrics
- ✅ Generates dashboard-ready outputs
- ✅ Can be explained in under 5 minutes
- ✅ Runs in under 10 seconds

**Next Action:** Open TEAM_GUIDE.md and assign roles to your team!

---

🚀 **Good luck with your KATA!** 🚀

*Remember: Focus on clarity and correctness over perfection. You can always iterate and improve after the initial hour.*
