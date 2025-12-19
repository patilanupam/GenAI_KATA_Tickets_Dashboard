# Setup Guide - Virtual Environment & Boilerplate Code

## Quick Start (5 Minutes)

Your virtual environment is already created and all libraries are installed!

### Windows Users:
```cmd
# Option 1: Double-click this file
activate_venv.bat

# Option 2: Command line
venv\Scripts\activate
```

### Mac/Linux Users:
```bash
# Activate venv
source activate_venv.sh
# or
source venv/bin/activate
```

---

## What's Been Set Up

### 1. Virtual Environment ✅
- Location: `venv/` folder
- Python version: Same as your system Python
- Isolated from system packages

### 2. Installed Libraries ✅

**Core Data Processing:**
- pandas (2.0.0+) - Data manipulation
- numpy (1.24.0+) - Numerical computing
- python-dateutil (2.8.0+) - Date handling

**Visualization:**
- matplotlib (3.7.0+) - Plotting
- seaborn (0.12.0+) - Statistical visualization

**Dashboard (Optional):**
- streamlit (1.28.0+) - Interactive web dashboard

**Excel Export:**
- openpyxl (3.1.0+) - Read/write Excel files
- xlsxwriter (3.1.0+) - Excel formatting

**Data Validation:**
- pydantic (2.0.0+) - Data validation

**Testing:**
- pytest (7.4.0+) - Testing framework
- pytest-cov (4.1.0+) - Coverage reports

### 3. Boilerplate Code Created ✅

**Core Modules:**
1. `config.py` - Configuration management
2. `utils.py` - Helper functions
3. `data_loader.py` - Data loading & validation
4. `process_tickets.py` - Main processing script
5. `streamlit_app.py` - Web dashboard (optional)

**Support Files:**
1. `requirements.txt` - Dependency list
2. `activate_venv.bat` - Windows activation script
3. `activate_venv.sh` - Mac/Linux activation script

---

## Usage Instructions

### Step 1: Activate Virtual Environment

**Windows:**
```cmd
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` at the start of your command prompt.

### Step 2: Run the Main Script

```bash
python process_tickets.py
```

This will:
- Load ticket and effort data
- Clean and standardize data
- Calculate KPIs
- Generate output CSV files in `outputs/` folder

### Step 3: Test Individual Modules

**Test Configuration:**
```bash
python config.py
```

**Test Utilities:**
```bash
python utils.py
```

**Test Data Loader:**
```bash
python data_loader.py
```

### Step 4 (Optional): Launch Web Dashboard

```bash
streamlit run streamlit_app.py
```

This will open an interactive dashboard in your browser at `http://localhost:8501`

---

## Project Structure

```
KATA_Tickets_Dashboard/
│
├── venv/                          # Virtual environment (DO NOT COMMIT)
│
├── data/                          # Input data folder
│   ├── tickets 1.csv             # Ticket data
│   └── effort 1.csv              # Effort data
│
├── outputs/                       # Generated outputs
│   ├── tickets_master.csv
│   ├── kpi_monthly_summary.csv
│   └── agent_performance.csv
│
├── logs/                          # Logs (future use)
│
├── config.py                      # Configuration file
├── utils.py                       # Utility functions
├── data_loader.py                 # Data loading module
├── process_tickets.py             # Main processing script
├── streamlit_app.py               # Web dashboard
│
├── requirements.txt               # Python dependencies
├── activate_venv.bat              # Windows activation
├── activate_venv.sh               # Unix activation
│
├── README.md                      # Main documentation
├── TEAM_GUIDE.md                  # Team instructions
├── ARCHITECTURE.md                # System architecture
├── USER_MANUAL.md                 # User guide
└── SETUP_GUIDE.md                 # This file
```

---

## Boilerplate Code Overview

### config.py - Configuration Management

**Purpose:** Centralized configuration for paths, constants, and business rules

**Key Features:**
- Path management (input/output directories)
- Data schema definitions
- Business rules (SLA thresholds, CSAT categories)
- Helper functions

**Example Usage:**
```python
import config

# Access configuration
print(config.INPUT_TICKETS_FILE)
print(config.CSAT_HIGH_THRESHOLD)

# Ensure directories exist
config.ensure_directories()
```

---

### utils.py - Utility Functions

**Purpose:** Reusable helper functions for data processing

**Key Features:**
- Date/time utilities (parsing, formatting)
- Data validation functions
- Data cleaning functions
- Feature engineering (SLA, CSAT categorization)
- Aggregation helpers
- Export utilities

**Example Usage:**
```python
import pandas as pd
import utils

# Parse dates
df['date'] = utils.parse_datetime(df['date_string'])

# Calculate percentage
pct = utils.calculate_percentage(75, 100)  # Returns 75.0

# Categorize CSAT
df = utils.categorize_csat(df)
```

---

### data_loader.py - Data Loading Module

**Purpose:** Handle loading and validation of input data

**Key Features:**
- Load tickets data with error handling
- Load effort data with error handling
- Data quality checks
- Column validation
- Sample data generation (for testing)

**Example Usage:**
```python
import data_loader

# Load all data
tickets_df, effort_df = data_loader.load_all_data()

# Run quality checks
data_loader.check_data_quality(tickets_df, effort_df)

# Generate sample data for testing
sample_df = data_loader.generate_sample_tickets(100)
```

---

### streamlit_app.py - Web Dashboard

**Purpose:** Interactive web dashboard for visualizing metrics

**Key Features:**
- Real-time filtering (hub, function)
- Key metrics cards
- Interactive charts
- Hub comparison
- Agent performance tracking
- Detailed data table with search
- CSV export

**To Run:**
```bash
streamlit run streamlit_app.py
```

---

## Common Tasks

### Task 1: Process New Data

1. Replace `tickets 1.csv` and `effort 1.csv` with new data
2. Run: `python process_tickets.py`
3. Check `outputs/` folder for results

### Task 2: Add New KPI

1. Edit `process_tickets.py`
2. Add calculation in the KPI computation section
3. Update column list in output
4. Run script to test

### Task 3: Customize Dashboard

1. Edit `streamlit_app.py`
2. Add new charts or metrics
3. Run: `streamlit run streamlit_app.py`
4. View changes in browser

### Task 4: Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'pandas'"

**Solution:** Make sure virtual environment is activated
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Issue: "FileNotFoundError: tickets 1.csv"

**Solution:** Make sure CSV files are in the correct location
```bash
# Check current directory
pwd  # Mac/Linux
cd   # Windows

# List files
ls   # Mac/Linux
dir  # Windows
```

### Issue: Virtual environment activation not working

**Windows Solution:**
```cmd
# Enable script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Mac/Linux Solution:**
```bash
# Make script executable
chmod +x activate_venv.sh
```

### Issue: Streamlit not opening in browser

**Solution:**
```bash
# Manually open in browser
# Go to: http://localhost:8501
```

---

## Deactivating Virtual Environment

When you're done working:

```bash
deactivate
```

This returns you to your system Python environment.

---

## Adding New Libraries

If you need additional libraries:

```bash
# Activate venv first
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install new library
pip install library-name

# Update requirements.txt
pip freeze > requirements.txt
```

---

## Git Best Practices

### What to Commit:
✅ All `.py` files
✅ `requirements.txt`
✅ `.md` documentation files
✅ Sample data (if small)

### What NOT to Commit:
❌ `venv/` folder
❌ `outputs/` folder
❌ `logs/` folder
❌ `__pycache__/` folders
❌ `.pyc` files
❌ Large CSV files

**Create `.gitignore` file:**
```
# Virtual Environment
venv/
env/
ENV/

# Outputs
outputs/
logs/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so

# Jupyter
.ipynb_checkpoints

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

---

## Next Steps

1. ✅ Virtual environment is ready
2. ✅ All libraries installed
3. ✅ Boilerplate code created

**Now you can:**
- Run `python process_tickets.py` to process data
- Launch `streamlit run streamlit_app.py` for dashboard
- Customize the code for your needs
- Add new features and KPIs

---

## Learning Resources

### Python & Pandas
- [Pandas Cheat Sheet](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

### Streamlit
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Gallery](https://streamlit.io/gallery)

### Data Visualization
- [Matplotlib Tutorial](https://matplotlib.org/stable/tutorials/index.html)
- [Seaborn Tutorial](https://seaborn.pydata.org/tutorial.html)

---

## Support

**Need Help?**
- Check the error message carefully
- Review the USER_MANUAL.md
- Test individual modules (config.py, utils.py, data_loader.py)
- Check that venv is activated
- Verify CSV files exist in correct location

---

## Summary

You now have:
- ✅ Isolated virtual environment
- ✅ All required libraries installed
- ✅ Modular, reusable code structure
- ✅ Configuration management
- ✅ Data loading with validation
- ✅ Utility functions
- ✅ Interactive dashboard
- ✅ Complete documentation

**Ready to start coding!** 🚀

---

*Created for: KATA Tickets Dashboard Project*
*Date: 2025-12-19*
