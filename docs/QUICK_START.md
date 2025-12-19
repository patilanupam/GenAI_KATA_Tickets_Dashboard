# 🚀 Quick Start Guide

## Your Environment is Ready!

Everything has been set up for you. Here's how to get started in 3 easy steps:

---

## Step 1: Activate Virtual Environment

### Windows (Choose one):
```cmd
# Option A: Double-click this file
activate_venv.bat

# Option B: Command line
venv\Scripts\activate
```

### Mac/Linux:
```bash
source activate_venv.sh
```

**You'll see `(venv)` at the start of your prompt when activated.**

---

## Step 2: Run the Application

### Quick Run (Recommended):
**Windows:**
```cmd
run_all.bat
```

**Mac/Linux:**
```bash
bash run_all.sh
```

### Manual Run:
```bash
# Process ticket data
python process_tickets.py

# Launch web dashboard (optional)
streamlit run streamlit_app.py
```

---

## Step 3: View Results

After running the script, check the `outputs/` folder:
- `tickets_master.csv` - Clean ticket data
- `kpi_monthly_summary.csv` - KPI metrics
- `agent_performance.csv` - Agent metrics

---

## What's Installed?

All libraries are ready to use in your virtual environment:

**Core:**
- pandas, numpy - Data processing
- python-dateutil - Date handling

**Visualization:**
- matplotlib, seaborn - Charts
- streamlit - Interactive dashboard

**Excel:**
- openpyxl, xlsxwriter - Excel export

**Testing:**
- pytest, pytest-cov - Unit testing

---

## Available Scripts & Modules

### Main Scripts:
1. `process_tickets.py` - Process ticket data
2. `streamlit_app.py` - Web dashboard
3. `run_all.bat` / `run_all.sh` - Quick run

### Modules (Boilerplate):
1. `config.py` - Configuration management
2. `utils.py` - Helper functions
3. `data_loader.py` - Data loading & validation

### Test Modules:
```bash
# Test configuration
python config.py

# Test utilities
python utils.py

# Test data loader
python data_loader.py
```

---

## File Structure

```
KATA_Tickets_Dashboard/
├── venv/                      # Virtual environment ✅
├── outputs/                   # Generated reports
│
├── process_tickets.py         # Main script
├── streamlit_app.py           # Dashboard
├── config.py                  # Config
├── utils.py                   # Utilities
├── data_loader.py             # Data loader
│
├── run_all.bat/.sh            # Quick run
├── activate_venv.bat/.sh      # Activate venv
│
├── requirements.txt           # Dependencies ✅
├── .gitignore                 # Git ignore
│
├── README.md                  # Main docs
├── TEAM_GUIDE.md              # Team guide
├── SETUP_GUIDE.md             # Setup details
├── QUICK_START.md             # This file
└── USER_MANUAL.md             # User manual
```

---

## Common Commands

```bash
# Activate virtual environment
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux

# Process data
python process_tickets.py

# Launch dashboard
streamlit run streamlit_app.py

# Run tests
pytest

# Deactivate venv
deactivate
```

---

## Troubleshooting

### Virtual environment not activating?
- **Windows:** Run `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`
- **Mac/Linux:** Run `chmod +x activate_venv.sh`

### Module not found?
- Make sure venv is activated (you should see `(venv)` in prompt)
- Run `pip list` to see installed packages

### File not found errors?
- Make sure you're in the correct directory
- Check that CSV files exist

---

## Next Steps

### For Beginners:
1. Read `TEAM_GUIDE.md` for role assignments
2. Run `python process_tickets.py`
3. Open outputs in Excel
4. Create simple dashboard

### For Advanced Users:
1. Customize `config.py` for your needs
2. Add new functions to `utils.py`
3. Extend KPI calculations
4. Build custom Streamlit dashboard

---

## Key Features

### Modular Code Structure ✅
- Separate files for config, utilities, and data loading
- Easy to extend and customize
- Well-documented with comments

### Data Processing ✅
- Load and clean ticket data
- Calculate KPIs (SLA, CSAT, volume)
- Generate dashboard-ready outputs

### Interactive Dashboard ✅
- Real-time filtering
- Multiple visualizations
- Hub and agent comparisons

### Testing Framework ✅
- pytest configured
- Coverage reporting
- Quality checks built-in

---

## Example Workflow

```bash
# 1. Start your session
venv\Scripts\activate

# 2. Process new data
python process_tickets.py

# 3. View results
# Open outputs/kpi_monthly_summary.csv in Excel

# 4. Launch dashboard (optional)
streamlit run streamlit_app.py

# 5. End session
deactivate
```

---

## Help & Resources

**Documentation:**
- `README.md` - Project overview
- `TEAM_GUIDE.md` - Team instructions (4 people)
- `SETUP_GUIDE.md` - Detailed setup
- `USER_MANUAL.md` - User guide

**Support:**
- Check error messages carefully
- Review the documentation
- Test individual modules
- Ensure venv is activated

---

## Summary

You have:
- ✅ Virtual environment with all libraries installed
- ✅ Modular boilerplate code (config, utils, data_loader)
- ✅ Main processing script (process_tickets.py)
- ✅ Interactive dashboard (streamlit_app.py)
- ✅ Quick run scripts (run_all.bat/.sh)
- ✅ Complete documentation
- ✅ Git configuration (.gitignore)

**You're ready to start!** 🎉

---

## Quick Reference

| Task | Command |
|------|---------|
| Activate venv | `venv\Scripts\activate` (Win) or `source venv/bin/activate` (Unix) |
| Process data | `python process_tickets.py` |
| Launch dashboard | `streamlit run streamlit_app.py` |
| Quick run | `run_all.bat` (Win) or `bash run_all.sh` (Unix) |
| Deactivate | `deactivate` |
| Install new lib | `pip install package-name` |
| Update requirements | `pip freeze > requirements.txt` |

---

**Ready? Let's go!** 🚀

Run `run_all.bat` (Windows) or `bash run_all.sh` (Mac/Linux) to get started!
