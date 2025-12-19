# Support Operations Performance Dashboard

**A complete end-to-end data analytics solution for unified support operations reporting across multiple hubs.**

🚀 **[Live Dashboard: https://orion-tickets-dashboard.streamlit.app/](https://orion-tickets-dashboard.streamlit.app/)**

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white)](https://plotly.com/)

---

## 📋 Overview

This solution processes support ticket data from multiple hubs (ServiceNow, Jira Service Management) and generates a comprehensive interactive dashboard for performance analysis and reporting.

**Key Features:**
- 🎯 **5 Interactive Dashboard Tabs** with 20+ visualizations
- 📊 **30+ KPIs** automatically calculated
- 🔄 **Real-time Filtering** by Hub, Function, and Date Range
- 📥 **Export Functionality** for all reports
- 🤖 **Auto-Generated Insights** for management
- ⚡ **Fast Processing** - handles data in seconds

---

## 🏗️ Architecture

### System Design

```
┌─────────────────────────────────────────────────────────────────┐
│                         DATA SOURCES                            │
│  ┌──────────────────────┐      ┌──────────────────────┐        │
│  │  Hub A (Bangalore)   │      │  Hub B (Krakow)      │        │
│  │  ServiceNow Export   │      │  Jira Export         │        │
│  │  tickets 1.csv       │      │  effort 1.csv        │        │
│  └──────────────────────┘      └──────────────────────┘        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    DATA PROCESSING LAYER                         │
│                         (main.py)                                │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  STEP 1: Load Data          - Read CSV files           │    │
│  │  STEP 2: Clean & Transform  - Parse dates, normalize   │    │
│  │  STEP 3: Enrich Data        - Calculate metrics        │    │
│  │  STEP 4: Compute KPIs       - Aggregate by groups      │    │
│  │  STEP 5: Agent Performance  - Calculate utilization    │    │
│  └────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                       OUTPUT LAYER                               │
│  ┌───────────────────┐  ┌───────────────────┐  ┌─────────────┐ │
│  │ tickets_master    │  │ kpi_monthly       │  │ agent_      │ │
│  │ .csv (150 rows)   │  │ _summary.csv      │  │ performance │ │
│  │                   │  │ (18 rows)         │  │ .csv        │ │
│  └───────────────────┘  └───────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   VISUALIZATION LAYER                            │
│                         (app.py)                                 │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Tab 1: Volume & Distribution View                     │    │
│  │  Tab 2: SLA & Resolution Performance                   │    │
│  │  Tab 3: CSAT Analysis                                  │    │
│  │  Tab 4: Management Summary Report                      │    │
│  │  Tab 5: Detailed KPI Table + Agent Metrics             │    │
│  └────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    STREAMLIT CLOUD                               │
│              https://your-app.streamlit.app                      │
└─────────────────────────────────────────────────────────────────┘
```

**📚 Detailed Architecture:** See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

## 🛠️ Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.9+ | Core programming language |
| **Pandas** | Latest | Data manipulation and analysis |
| **Streamlit** | Latest | Interactive web dashboard framework |
| **Plotly** | Latest | Interactive visualizations |
| **CSV** | - | Data storage format (simple, portable) |

### Why These Technologies?

- **Python + Pandas**: Industry standard for data processing, easy to learn
- **Streamlit**: Rapid dashboard development, no frontend coding needed
- **Plotly**: Interactive charts with hover tooltips and zoom capabilities
- **CSV**: Universal format, works with Excel, databases, and all tools

---

## 📊 What We Built

### 5 Interactive Dashboard Tabs

#### 1️⃣ Volume & Distribution View
- Monthly ticket volume trends (line chart)
- Hub A vs Hub B distribution (pie chart)
- Function breakdown: IT/HR/Finance (pie chart)
- Top 10 categories (bar chart)
- Channel distribution: Email/Portal/Phone/Chat (bar chart)
- Priority distribution over time (stacked bar chart)

#### 2️⃣ SLA & Resolution Performance View
- SLA compliance trend with 80% target line
- Average resolution time trend
- Hub A vs Hub B comparison (3 metrics)
- Top 5 worst categories by SLA
- Top 5 categories by resolution time
- Detailed category performance table

#### 3️⃣ CSAT Analysis View
- Average CSAT by hub (with 4.0 target line)
- Average CSAT by function
- CSAT trend over time
- CSAT distribution (1-5 scale)
- Top 10 categories by CSAT score

#### 4️⃣ Management Summary Report
- Last month KPIs (5 key metrics)
- Auto-generated Top 3 Improvement Areas
- Auto-generated Top 3 Positive Highlights
- Top performing categories
- Top performing agents
- Recommended action items

#### 5️⃣ Detailed KPI Table + Agent Metrics
- Complete KPI table (30+ metrics)
- Breakdown tables (channel, priority, SLA, CSAT)
- Hub-wise and function-wise comparisons
- Month-over-month trends
- **Comprehensive Agent Metrics Section:**
  - Agent performance by month
  - Tickets per agent analysis
  - Utilization % tracking (with 100% capacity line)
  - Performance trends over time
  - Efficiency metrics (6 key metrics)

### Global Features
- **Filters**: Apply Hub, Function, Date Range across all tabs
- **Export**: Download CSV from any tab
- **Interactive Charts**: Hover tooltips, zoom, pan
- **Color-Coded Insights**: Green (positive), Red (needs attention)

---

## 🚀 Quick Start

### Prerequisites

```bash
# Check Python version (3.9+ required)
python --version

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### Installation

```bash
# Clone repository
git clone https://github.com/patilanupam/GenAI_KATA_Tickets_Dashboard.git
cd GenAI_KATA_Tickets_Dashboard

# Install dependencies
pip install -r requirements.txt
```

### Run Locally

```bash
# Step 1: Process data (generates outputs)
python main.py

# Step 2: Launch dashboard
streamlit run app.py
```

Dashboard will open at: http://localhost:8501

---

## 📁 Project Structure

```
GenAI_KATA_Tickets_Dashboard/
├── .streamlit/
│   └── config.toml              # Streamlit theme configuration
│
├── data/                        # Input data files
│   ├── tickets 1.csv            # Ticket data (150 records)
│   └── effort 1.csv             # Agent effort data (21 records)
│
├── docs/                        # 📚 Detailed Documentation
│   ├── ARCHITECTURE.md          # System design details
│   ├── USER_MANUAL.md           # Complete user guide
│   ├── PROJECT_STRUCTURE.md     # File organization
│   ├── QUICK_START.md           # Getting started guide
│   └── ... (6 more docs)
│
├── outputs/                     # Generated files
│   ├── tickets_master.csv       # Processed ticket data
│   ├── kpi_monthly_summary.csv  # Monthly KPI metrics
│   └── agent_performance.csv    # Agent performance data
│
├── app.py                       # Main Streamlit dashboard (1450 lines)
├── main.py                      # Data processing pipeline (237 lines)
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
├── DEPLOYMENT_GUIDE.md          # How to deploy to Streamlit Cloud
└── README.md                    # This file
```

---

## 🎯 Core KPIs Computed

### Ticket Volume Metrics
- Total tickets
- Tickets by channel (Email, Portal, Phone, Chat)
- Tickets by priority (Critical, High, Medium, Low)
- Tickets by category (all categories)

### SLA & Resolution Performance
- SLA Compliance % (per month/hub/function)
- Average Resolution Time (hours)
- Backlog at Month-End
- Reopen Rate %

### Customer Satisfaction (CSAT)
- Average CSAT Score (1-5 scale)
- % High Satisfaction (CSAT ≥ 4)
- % Low Satisfaction (CSAT ≤ 2)

### Agent Metrics
- Tickets per Agent per Month
- Ticket Work Utilization %
- Average Hours per Ticket
- Agent performance trends

**Total: 30+ metrics computed and visualized**

---

## 🔧 How to Create This Yourself

### Step-by-Step Implementation Guide

#### Step 1: Data Processing (main.py)

```python
# Load data
import pandas as pd
tickets_df = pd.read_csv("data/tickets 1.csv")
effort_df = pd.read_csv("data/effort 1.csv")

# Parse dates and extract time features
tickets_df['created_datetime'] = pd.to_datetime(tickets_df['created_datetime'])
tickets_df['year_month'] = tickets_df['created_datetime'].dt.to_period('M')

# Calculate resolution time
tickets_df['resolution_time_hours'] = (
    tickets_df['resolved_datetime'] - tickets_df['created_datetime']
).dt.total_seconds() / 3600

# Calculate SLA compliance
tickets_df['sla_met'] = (
    tickets_df['resolution_time_hours'] <= tickets_df['sla_target_hours']
)

# Group and aggregate KPIs
kpi_summary = tickets_df.groupby(['year_month', 'hub', 'function']).agg({
    'ticket_id': 'count',  # total tickets
    'sla_met': 'mean',     # SLA compliance %
    'resolution_time_hours': 'mean',  # avg resolution time
    'csat_score': 'mean'   # avg CSAT
}).reset_index()

# Save outputs
kpi_summary.to_csv("outputs/kpi_monthly_summary.csv", index=False)
```

**📚 Complete Code:** See [main.py](main.py)

#### Step 2: Dashboard Creation (app.py)

```python
import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    tickets = pd.read_csv("outputs/tickets_master.csv")
    kpis = pd.read_csv("outputs/kpi_monthly_summary.csv")
    agents = pd.read_csv("outputs/agent_performance.csv")
    return tickets, kpis, agents

# Create sidebar filters
st.sidebar.header("Filters")
selected_hub = st.sidebar.selectbox("Hub", ['All', 'A', 'B'])
selected_function = st.sidebar.selectbox("Function", ['All', 'IT', 'HR', 'Finance'])

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Volume & Distribution",
    "SLA Performance",
    "CSAT Analysis",
    "Management Summary",
    "Detailed KPIs"
])

# Add visualizations to each tab
with tab1:
    fig = px.line(data, x='month', y='ticket_count', color='hub')
    st.plotly_chart(fig)
```

**📚 Complete Code:** See [app.py](app.py)

#### Step 3: Configuration Files

**requirements.txt:**
```
pandas
streamlit
plotly
```

**.streamlit/config.toml:**
```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"

[server]
headless = true
port = 8501
```

#### Step 4: Deploy to Streamlit Cloud

1. Push code to GitHub
2. Go to https://share.streamlit.io/
3. Connect your repository
4. Set main file: `app.py`
5. Deploy!

**📚 Detailed Deployment Guide:** See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

## 📖 Documentation

All detailed documentation is in the `docs/` folder:

| Document | Description |
|----------|-------------|
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | Complete system architecture and data flow |
| [USER_MANUAL.md](docs/USER_MANUAL.md) | Comprehensive user guide for the dashboard |
| [PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) | Detailed file organization explanation |
| [QUICK_START.md](docs/QUICK_START.md) | 3-step getting started guide |
| [SETUP_GUIDE.md](docs/SETUP_GUIDE.md) | Technical setup and installation |
| [FINAL_VERIFICATION.md](docs/FINAL_VERIFICATION.md) | Quality criteria verification |
| [KATA_REQUIREMENTS_CHECKLIST.md](docs/KATA_REQUIREMENTS_CHECKLIST.md) | Complete requirements check |
| [COMPLETE_ANALYSIS_VERIFICATION.md](docs/COMPLETE_ANALYSIS_VERIFICATION.md) | Analysis completeness verification |

**Plus:** [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) in root for Streamlit Cloud deployment

---

## 🎨 Design Principles

### SOLID Principles
- **Single Responsibility**: `main.py` handles data processing, `app.py` handles visualization
- **Open/Closed**: Easy to add new KPIs without modifying existing code
- **Interface Segregation**: Focused, modular functions
- **Dependency Inversion**: Uses pandas/streamlit abstractions

### KISS (Keep It Simple, Stupid)
- CSV files instead of complex databases
- Direct pandas operations without unnecessary abstractions
- Streamlit for simple web UI (no React/Angular complexity)

### YAGNI (You Aren't Gonna Need It)
- No database (CSV sufficient for data volume)
- No authentication (not required for MVP)
- No CI/CD (not required initially)
- No complex caching (data volume doesn't require it)

---

## 🔄 Data Flow

```
Input CSVs
    ↓
Load (pandas.read_csv)
    ↓
Clean (parse dates, normalize values)
    ↓
Transform (calculate metrics, enrich)
    ↓
Aggregate (groupby month/hub/function)
    ↓
Output CSVs (tickets_master, kpi_summary, agent_performance)
    ↓
Load into Streamlit
    ↓
Apply Filters (hub, function, date range)
    ↓
Render Visualizations (plotly charts)
    ↓
Interactive Dashboard
```

---

## 📈 Sample Results

**Dataset:** 150 tickets, Oct-Dec 2025, 2 hubs, 3 functions, 7 agents

**Key Metrics:**
- Total Tickets: 150
- Hub A: 77 tickets (51%)
- Hub B: 73 tickets (49%)
- Overall SLA Compliance: 41.4%
- Average Resolution Time: 28.7 hours
- Average CSAT: 3.20/5
- Current Backlog: 51 tickets

**Performance:**
- Data Processing Time: <5 seconds
- Dashboard Load Time: <3 seconds
- Interactive Response: Real-time

---

## 🚀 Deployment

### Option 1: Local Deployment

```bash
streamlit run app.py
```

Access at: http://localhost:8501

### Option 2: Streamlit Cloud (Recommended)

**Live Dashboard:** Your app will be deployed at:
```
https://your-app-name.streamlit.app
```

**Benefits:**
- ✅ Free hosting
- ✅ Automatic updates from GitHub
- ✅ HTTPS enabled
- ✅ Shareable public URL
- ✅ No server management

**📚 Step-by-Step Guide:** See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

## 🔍 Key Features Explained

### Global Filters
All filters apply across all 5 tabs simultaneously:
- **Hub Filter**: View All hubs, Hub A only, or Hub B only
- **Function Filter**: Filter by IT, HR, Finance, or All
- **Date Range**: Select custom date range for analysis

### Auto-Generated Insights
The dashboard automatically identifies:
- **Top 3 Improvement Areas**: Based on thresholds (low SLA, high backlog, etc.)
- **Top 3 Positive Highlights**: Based on high performance (high SLA, high CSAT, etc.)

### Export Functionality
Every tab has a download button to export filtered data as CSV for:
- Further analysis in Excel
- Reports for stakeholders
- Data backup

### Interactive Visualizations
All charts support:
- Hover tooltips with detailed data
- Zoom and pan
- Legend click to show/hide series
- Responsive design for all screen sizes

---

## 🛡️ Data Quality

### Input Data Validation
- Date parsing with error handling
- CSAT score normalization (1-5 scale)
- SLA target validation
- Agent ID mapping verification

### Output Data Quality
- All 150 tickets accounted for
- 100% agent attribution (no orphaned tickets)
- Month alignment verified (Oct-Dec 2025)
- KPI calculations validated

---

## ⚙️ Customization

### Adding New KPIs

Edit `main.py`:
```python
# Add new KPI calculation
kpi_summary['new_metric'] = grouped_data['column'].agg('function')
```

### Adding New Visualizations

Edit `app.py`:
```python
# Add new chart in any tab
fig = px.bar(data, x='category', y='value')
st.plotly_chart(fig)
```

### Changing Theme

Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#YOUR_COLOR"
backgroundColor = "#YOUR_COLOR"
```

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: "FileNotFoundError"
**Solution:** Run `main.py` first to generate outputs
```bash
python main.py
```

### Issue: Dashboard shows no data
**Solution:** Check filters - reset to "All" in sidebar

### Issue: Agent metrics showing 0
**Solution:** Verify effort data months align with ticket months

**📚 Complete Troubleshooting:** See [docs/USER_MANUAL.md](docs/USER_MANUAL.md)

---

## 📊 Business Value

This dashboard enables leadership to answer:

1. **Volume**: How many tickets are we handling per month?
2. **Comparison**: Which hub performs better on SLA?
3. **Trends**: Are CSAT scores improving or declining?
4. **Categories**: What are the most common problem types?
5. **Efficiency**: Are agents over or under-utilized?
6. **Backlog**: Do we have a growing backlog problem?
7. **Investment**: Where should we allocate resources?

---

## 🔮 Future Enhancements

### Phase 1 (Immediate)
- [ ] Add more data validation checks
- [ ] Implement error handling for missing data
- [ ] Add unit tests for KPI calculations

### Phase 2 (Short-term)
- [ ] Integrate with live APIs (ServiceNow, Jira)
- [ ] Add authentication for private deployment
- [ ] Implement scheduled data refresh

### Phase 3 (Long-term)
- [ ] Move to database (PostgreSQL)
- [ ] Add predictive analytics (ML models)
- [ ] Implement alerting for SLA breaches
- [ ] Create mobile-responsive version

---

## 📜 License

This project is created for educational purposes (KATA challenge).
Feel free to use, modify, and extend for your own projects.

---

## 🙏 Acknowledgments

- Built with **Claude Code** (Anthropic's AI coding assistant)
- Powered by **Streamlit** open-source framework
- Data processing with **Pandas** library
- Visualizations by **Plotly**

---

## 📞 Support

- **Documentation**: Check [docs/](docs/) folder for detailed guides
- **Issues**: Report bugs via GitHub Issues
- **Streamlit Help**: https://docs.streamlit.io/
- **Pandas Help**: https://pandas.pydata.org/docs/

---

## ✅ Success Checklist

Before deploying, ensure:

- [ ] `main.py` runs without errors
- [ ] All 3 output CSVs generated in `outputs/` folder
- [ ] Dashboard loads at http://localhost:8501
- [ ] All 5 tabs display correctly
- [ ] All filters work (Hub, Function, Date Range)
- [ ] All visualizations show data
- [ ] Download buttons work
- [ ] Agent metrics section shows data (not "No data")
- [ ] Top Performing Agents populated

---

## 📊 Live Demo

**Repository:** https://github.com/patilanupam/GenAI_KATA_Tickets_Dashboard

**Streamlit App:** Will be available after deployment at:
```
https://genai-kata-tickets-dashboard.streamlit.app
```

---

## 🚀 Getting Started Now

```bash
# Clone the repository
git clone https://github.com/patilanupam/GenAI_KATA_Tickets_Dashboard.git

# Navigate to project
cd GenAI_KATA_Tickets_Dashboard

# Install dependencies
pip install -r requirements.txt

# Process data
python main.py

# Launch dashboard
streamlit run app.py
```

**That's it! Your dashboard is now running locally.** 🎉

**Next step:** Deploy to Streamlit Cloud following [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

**Built with ❤️ using Python, Pandas, Streamlit, and AI**

*Last Updated: December 2025*
