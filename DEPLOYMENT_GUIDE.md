# Deployment Guide - Streamlit Cloud

Deploy your Support Operations Dashboard online in 3 simple steps.

## Prerequisites
- GitHub account (free): https://github.com/signup
- Streamlit Cloud account (free): https://share.streamlit.io/signup

## Step 1: Push to GitHub

```bash
cd "C:/Users/AnupamPatil/Documents/KATA_Tickets_Dashboard"

# Add all files
git add .

# Commit
git commit -m "Support Operations Dashboard - Complete Solution"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/support-ops-dashboard.git

# Push
git branch -M main
git push -u origin main
```

## Step 2: Deploy on Streamlit Cloud

1. Go to: https://share.streamlit.io/
2. Click "New app"  
3. Select your repository
4. Set main file: `app.py`
5. Click "Deploy"

Wait 2-3 minutes for deployment.

## Step 3: Access Your Dashboard

Your dashboard will be live at:
```
https://YOUR-APP-NAME.streamlit.app
```

Share this URL with your team!

## Updating the Dashboard

Push changes to GitHub - Streamlit auto-updates:

```bash
git add .
git commit -m "Update dashboard"
git push
```

## Troubleshooting

**Issue: Missing dependencies**
- Check `requirements.txt` contains: pandas, streamlit, plotly

**Issue: Data files not found**
- Ensure `data/` folder is in GitHub repo
- Check `.gitignore` doesn't exclude data files

**Issue: Dashboard shows error**
- View logs in Streamlit Cloud dashboard
- Fix error, test locally, then push

## Project Structure

```
support-ops-dashboard/
├── .streamlit/config.toml
├── data/
│   ├── tickets 1.csv
│   └── effort 1.csv
├── outputs/
│   ├── tickets_master.csv
│   ├── kpi_monthly_summary.csv
│   └── agent_performance.csv
├── docs/
│   └── (documentation files)
├── app.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Features

Your deployed dashboard includes:
- 5 interactive tabs
- 30+ KPIs
- Hub A vs Hub B comparison
- Agent performance metrics
- Download buttons for exports
- Global filters (Hub, Function, Date Range)

## Support

- Streamlit Docs: https://docs.streamlit.io/
- Community Forum: https://discuss.streamlit.io/

---

Dashboard is now live! Share the URL with stakeholders.
