# Support Operations Performance Reporting - Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                          DATA SOURCES                                │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
           ┌──────────────────────────────────────┐
           │   tickets 1.csv (Hub A & Hub B)      │
           │   - Contains ticket details          │
           │   - Both hubs in single file         │
           └──────────────────────────────────────┘
                                  │
           ┌──────────────────────────────────────┐
           │   effort 1.csv (Agent Workload)      │
           │   - Agent hours per month            │
           │   - Both hubs included               │
           └──────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    DATA PROCESSING LAYER (Python + Pandas)           │
│                                                                       │
│  Step 1: LOAD DATA                                                   │
│    → Read CSV files into pandas DataFrames                           │
│                                                                       │
│  Step 2: CLEAN & STANDARDIZE                                         │
│    → Parse dates (created_datetime, resolved_datetime)               │
│    → Handle missing values (CSAT scores, resolved dates)             │
│    → Normalize categorical values (priority, status)                 │
│                                                                       │
│  Step 3: ENRICH DATA                                                 │
│    → Calculate resolution time (hours)                               │
│    → Determine SLA compliance (met/missed)                           │
│    → Extract month/year from dates                                   │
│    → Flag open/closed tickets                                        │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      KPI COMPUTATION LAYER                           │
│                                                                       │
│  Compute metrics grouped by: Month, Hub, Function                    │
│                                                                       │
│  TICKET VOLUME KPIs:                                                 │
│    • Total tickets created                                           │
│    • Tickets by priority (Critical/High/Medium/Low)                  │
│    • Tickets by channel (Email/Portal/Phone/Chat)                    │
│    • Tickets by category                                             │
│                                                                       │
│  SLA & RESOLUTION KPIs:                                              │
│    • SLA compliance % (met vs missed)                                │
│    • Average resolution time (hours)                                 │
│    • Backlog count (Open + In Progress)                              │
│    • Reopen rate %                                                   │
│                                                                       │
│  CSAT KPIs:                                                          │
│    • Average CSAT score (1-5)                                        │
│    • % High satisfaction (CSAT >= 4)                                 │
│    • % Low satisfaction (CSAT <= 2)                                  │
│                                                                       │
│  AGENT METRICS:                                                      │
│    • Tickets per agent                                               │
│    • Utilization % (ticket hours / total hours)                      │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         OUTPUT LAYER                                 │
│                                                                       │
│  OUTPUT 1: tickets_master.csv                                        │
│    → Clean, standardized ticket data                                 │
│    → Ready for detailed analysis                                     │
│                                                                       │
│  OUTPUT 2: kpi_monthly_summary.csv                                   │
│    → Aggregated KPIs by month/hub/function                           │
│    → Dashboard-ready metrics                                         │
│                                                                       │
│  OUTPUT 3: agent_performance.csv                                     │
│    → Agent-level metrics                                             │
│    → Workload and efficiency data                                    │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    REPORTING / DASHBOARD LAYER                       │
│                                                                       │
│  Option 1: Excel Pivot Tables (Quickest for beginners)              │
│  Option 2: Power BI (Connect to CSV outputs)                         │
│  Option 3: Streamlit Dashboard (Optional Python app)                 │
│                                                                       │
│  KEY VISUALIZATIONS:                                                 │
│    • Monthly ticket volume trends (line chart)                       │
│    • SLA compliance by hub (bar chart)                               │
│    • CSAT trends over time (line chart)                              │
│    • Top 5 problem categories (bar chart)                            │
│    • Hub comparison dashboard                                        │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

## Technology Stack

| Layer | Technology | Why? |
|-------|-----------|------|
| Data Storage | CSV Files | Simple, no database setup needed |
| Processing | Python 3.x | Easy to learn, powerful for data |
| Data Manipulation | Pandas | Industry standard for data analysis |
| Date Handling | datetime | Built-in Python library |
| Visualization | Excel / Power BI | Familiar tools for business users |

## Data Flow

1. **Input**: Raw CSV files from ServiceNow (Hub A) and Jira (Hub B)
2. **Process**: Python script reads, cleans, and standardizes data
3. **Compute**: KPIs calculated using pandas groupby and aggregation
4. **Output**: Clean CSV files ready for dashboards
5. **Report**: Import outputs into Excel/Power BI for visualization

## Key Design Principles

- **KISS (Keep It Simple)**: No complex infrastructure, just Python + CSV
- **YAGNI (You Aren't Gonna Need It)**: Only build what's needed for KPIs
- **SOLID**: Modular functions for each processing step
- **Beginner-Friendly**: Clear variable names, extensive comments

## File Structure

```
KATA_Tickets_Dashboard/
├── tickets 1.csv                  # Input: Ticket data
├── effort 1.csv                   # Input: Agent effort data
├── process_tickets.py             # Main processing script
├── outputs/
│   ├── tickets_master.csv         # Clean ticket data
│   ├── kpi_monthly_summary.csv    # KPI metrics
│   └── agent_performance.csv      # Agent metrics
├── ARCHITECTURE.md                # This file
└── TEAM_GUIDE.md                  # Team roles and instructions
```

## Execution Time: 1 Hour Breakdown

- **15 min**: Understand requirements and data
- **25 min**: Write and test Python processing script
- **10 min**: Generate outputs and verify KPIs
- **10 min**: Prepare presentation / demo

## Next Steps

1. Review this architecture
2. Check TEAM_GUIDE.md for role assignments
3. Run process_tickets.py script
4. Validate outputs
5. Create dashboard in Excel/Power BI
