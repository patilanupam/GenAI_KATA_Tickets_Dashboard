# Team Guide - Support Operations Reporting KATA

## Team: 4 Members | Time Limit: 1 Hour

---

## Quick Start Checklist

Before you begin:
- [ ] All 4 team members have read this guide
- [ ] Python 3.x is installed on your machine
- [ ] pandas library is installed (`pip install pandas`)
- [ ] You have the two CSV files: `tickets 1.csv` and `effort 1.csv`
- [ ] Everyone knows their role assignment

---

## Team Roles & Responsibilities

### Person 1: Data Engineer (Lead)
**Time: Full hour**

**Responsibilities:**
1. Understand the data structure (15 min)
2. Run and troubleshoot the Python script (20 min)
3. Validate outputs (15 min)
4. Support other team members (10 min)

**Tasks Checklist:**
- [ ] Read ARCHITECTURE.md to understand the solution
- [ ] Open `tickets 1.csv` and `effort 1.csv` to inspect data
- [ ] Install pandas if not already installed: `pip install pandas`
- [ ] Run the script: `python process_tickets.py`
- [ ] Check that `outputs/` folder was created with 3 CSV files
- [ ] Open each output file to verify data looks correct
- [ ] Help Person 2 understand the KPI metrics
- [ ] Answer technical questions from the team

**Key Commands:**
```bash
# Check Python version
python --version

# Install pandas
pip install pandas

# Run the processing script
python process_tickets.py

# List output files
dir outputs  # Windows
ls outputs   # Mac/Linux
```

**Troubleshooting:**
- If pandas is not installed: `pip install pandas`
- If file not found: Make sure you're in the correct directory
- If encoding error: The CSV files should be UTF-8 encoded

---

### Person 2: Analytics Engineer (KPI Specialist)
**Time: Full hour**

**Responsibilities:**
1. Understand KPI requirements (10 min)
2. Review output data (20 min)
3. Create Excel dashboard (25 min)
4. Prepare insights for presentation (5 min)

**Tasks Checklist:**
- [ ] Read the KPI section in `instructions.md` (lines 118-142)
- [ ] Wait for Person 1 to generate output files
- [ ] Open `outputs/kpi_monthly_summary.csv` in Excel
- [ ] Create pivot tables for key metrics
- [ ] Create 4-5 charts for the dashboard
- [ ] Calculate Hub A vs Hub B comparison
- [ ] Note top 3 insights for presentation

**Dashboard Components to Create:**

1. **Ticket Volume Chart**
   - Line chart showing total tickets by month
   - Two lines: Hub A and Hub B

2. **SLA Compliance Chart**
   - Bar chart showing SLA compliance % by hub

3. **CSAT Trends**
   - Line chart showing average CSAT over time

4. **Top Categories**
   - Bar chart of tickets by category (use tickets_master.csv)

5. **Summary Table**
   - Key metrics for latest month
   - Compare Hub A vs Hub B side by side

**Excel Quick Guide:**
```
1. Open kpi_monthly_summary.csv in Excel
2. Insert > PivotTable
3. Drag fields to create summaries
4. Insert > Charts to visualize
5. Use conditional formatting for highlights
```

---

### Person 3: Business Analyst (Requirements & Presentation)
**Time: Full hour**

**Responsibilities:**
1. Document business requirements (10 min)
2. Review solution alignment (15 min)
3. Create presentation slides (30 min)
4. Practice presentation (5 min)

**Tasks Checklist:**
- [ ] Read `instructions.md` completely
- [ ] List the key business problems being solved
- [ ] Review ARCHITECTURE.md to understand the solution
- [ ] Create 5-7 presentation slides
- [ ] Prepare talking points for demo
- [ ] Identify 3 key insights from the data
- [ ] Create "What's Next" recommendations

**Presentation Outline:**

**Slide 1: Problem Statement**
- OrionEdge Corp has 2 support hubs
- No unified reporting
- Leadership lacks visibility
- Manual, time-consuming processes

**Slide 2: Solution Overview**
- Automated data processing with Python
- Standardized KPI calculations
- Dashboard-ready outputs
- Scalable architecture

**Slide 3: Architecture**
- Show the data flow diagram
- Input → Process → Output → Dashboard
- Technologies used: Python, Pandas, CSV

**Slide 4: Key Metrics**
- Ticket volume: X total tickets
- SLA compliance: Hub A vs Hub B
- CSAT scores: Average and trends
- Agent performance: Utilization rates

**Slide 5: Demo**
- Show the Python script running
- Display output files
- Walk through Excel dashboard

**Slide 6: Key Insights**
- Hub comparison (which performs better?)
- Problem categories (what issues are most common?)
- Trends (improving or declining?)

**Slide 7: Next Steps & Recommendations**
- Schedule weekly automated runs
- Add more data sources
- Implement real-time dashboard
- Train more team members

---

### Person 4: Quality Assurance & Documentation
**Time: Full hour**

**Responsibilities:**
1. Test the solution (20 min)
2. Document edge cases (15 min)
3. Create user manual (20 min)
4. Final review (5 min)

**Tasks Checklist:**
- [ ] Wait for Person 1 to generate outputs
- [ ] Manually verify sample calculations
- [ ] Check for data quality issues
- [ ] Document any problems found
- [ ] Create simple user manual
- [ ] Test with different scenarios
- [ ] Verify all deliverables are complete

**Testing Checklist:**

**Data Quality Tests:**
- [ ] Are there any null values in key fields?
- [ ] Do date ranges make sense?
- [ ] Are SLA calculations correct?
- [ ] Do ticket counts match between files?

**Calculation Verification:**
1. Pick one month/hub/function combination
2. Manually count tickets in tickets_master.csv
3. Compare with total_tickets in kpi_monthly_summary.csv
4. Verify SLA compliance % calculation
5. Check CSAT average calculation

**Sample Manual Calculation:**
```
Example: Hub A, IT, October 2025

Step 1: Filter tickets_master.csv for:
  - hub = A
  - function = IT
  - year_month = 2025-10

Step 2: Count rows = Total tickets

Step 3: Count sla_met = True / Total with SLA data = SLA %

Step 4: Average resolution_time_hours = Avg resolution time
```

**User Manual to Create:**

Create a file called `USER_MANUAL.md` with:
- How to install Python and pandas
- How to run the script
- What each output file contains
- How to import into Excel
- Common troubleshooting tips
- Contact information for support

---

## Timeline & Milestones

### Minutes 0-15: Setup & Understanding
- **All:** Read assigned sections
- **Person 1:** Install dependencies, test environment
- **Person 2:** Study KPI requirements
- **Person 3:** Read business context
- **Person 4:** Prepare test plan

### Minutes 15-35: Execution
- **Person 1:** Run Python script, generate outputs
- **Person 2:** Start creating Excel dashboard
- **Person 3:** Create presentation slides
- **Person 4:** Begin testing outputs

### Minutes 35-50: Refinement
- **Person 1:** Help troubleshoot issues
- **Person 2:** Finalize dashboard and insights
- **Person 3:** Complete presentation with real data
- **Person 4:** Complete user manual

### Minutes 50-60: Final Review & Presentation
- **All:** Review deliverables together
- **Person 3:** Practice presentation
- **All:** Do final demo run

---

## Deliverables Checklist

### Technical Deliverables
- [ ] `process_tickets.py` - Working Python script
- [ ] `outputs/tickets_master.csv` - Clean ticket data
- [ ] `outputs/kpi_monthly_summary.csv` - KPI metrics
- [ ] `outputs/agent_performance.csv` - Agent metrics

### Documentation Deliverables
- [ ] `ARCHITECTURE.md` - System architecture
- [ ] `TEAM_GUIDE.md` - This file
- [ ] `USER_MANUAL.md` - User manual (Person 4)

### Presentation Deliverables
- [ ] PowerPoint/Slides - 5-7 slides (Person 3)
- [ ] Excel Dashboard - With charts (Person 2)
- [ ] Demo script - What to say and show

---

## Communication Plan

### Team Sync Points

**15-minute check-in:**
- Person 1: Update on script status
- Quick blockers discussion
- Adjust plan if needed

**35-minute check-in:**
- Person 1: Confirm outputs are ready
- Person 2: Show dashboard progress
- Person 3: Share presentation draft
- Person 4: Report test results

**50-minute final sync:**
- Review all deliverables
- Practice presentation once
- Assign speaking roles

### Who to Ask for Help

**Technical issues with Python:**
→ Ask Person 1 (Data Engineer)

**KPI calculation questions:**
→ Ask Person 2 (Analytics Engineer)

**Business context or presentation:**
→ Ask Person 3 (Business Analyst)

**Data quality issues:**
→ Ask Person 4 (QA)

---

## Key Concepts Explained (For Beginners)

### What is a CSV file?
A Comma-Separated Values file is a simple spreadsheet format that can be opened in Excel or processed with Python. Each line is a row, and commas separate the columns.

### What is Pandas?
A Python library that makes working with data easy. Think of it as Excel inside Python - you can filter, calculate, and transform data.

### What is a KPI?
Key Performance Indicator - a measurable value that shows how well the business is performing. Examples: ticket volume, SLA compliance %, average CSAT.

### What is SLA?
Service Level Agreement - a promise to resolve tickets within a certain time. If a ticket takes longer, the SLA is "missed."

### What is CSAT?
Customer Satisfaction score - typically rated 1-5, where 5 is very satisfied and 1 is very unsatisfied.

---

## Success Criteria

Your solution is successful if:
- ✅ The Python script runs without errors
- ✅ All 3 output CSV files are generated
- ✅ KPI calculations are accurate (spot-checked)
- ✅ Excel dashboard shows clear visualizations
- ✅ Presentation tells a clear story
- ✅ Solution can be explained in 5 minutes

---

## Common Mistakes to Avoid

1. **Don't over-engineer**: Keep it simple, you only have 1 hour
2. **Don't ignore errors**: If the script fails, fix it immediately
3. **Don't work in silos**: Communicate frequently
4. **Don't skip testing**: Verify calculations are correct
5. **Don't forget the business context**: This is for leadership, not just technical

---

## After the KATA

### If you have extra time:
1. Add more visualizations to the dashboard
2. Create a Streamlit app for interactive dashboards
3. Add data validation checks in the script
4. Write unit tests for key functions
5. Create a scheduled task to run weekly

### Learning Resources:
- Pandas documentation: https://pandas.pydata.org/docs/
- Python datetime: https://docs.python.org/3/library/datetime.html
- Excel pivot tables: https://support.microsoft.com/excel

---

## Questions & Answers

**Q: What if we don't have Python installed?**
A: Download from python.org - get Python 3.8 or newer. Then run `pip install pandas`.

**Q: Can we modify the Python script?**
A: Yes! It's designed to be beginner-friendly. Add comments if you make changes.

**Q: What if the KPIs don't match our manual calculations?**
A: Check the grouping logic (month/hub/function). Debug step by step.

**Q: Do we need to present to real leadership?**
A: This is a practice KATA. Present to your team or instructor as if they were leadership.

**Q: What if we run out of time?**
A: Prioritize: Working script > KPI outputs > Dashboard > Presentation. Get the basics working first.

---

## Contact & Support

**During the KATA:**
- Use team chat for quick questions
- Share screens to troubleshoot together
- Don't hesitate to ask for help

**After the KATA:**
- Review the solution together
- Discuss what went well and what didn't
- Plan improvements for next time

---

## Good Luck! 🚀

Remember:
- **Work together** - you're a team
- **Communicate often** - sync at 15, 35, and 50 minutes
- **Keep it simple** - don't over-engineer
- **Focus on value** - solve the business problem
- **Have fun** - this is a learning experience!

---

*This guide was created for beginners tackling a 1-hour KATA challenge. The solution is intentionally simple and educational, not production-grade.*
