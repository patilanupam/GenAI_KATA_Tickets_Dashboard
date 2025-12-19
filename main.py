"""
Main Entry Point for Support Operations Reporting System
Run this file to process all data and generate reports
"""

import pandas as pd
import os
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

print("\n")
print("=" * 80)
print(" " * 20 + "SUPPORT OPERATIONS REPORTING SYSTEM")
print(" " * 25 + "OrionEdge Corp - 2025")
print("=" * 80)
print("\n")

INPUT_TICKETS = "data/tickets 1.csv"
INPUT_EFFORT = "data/effort 1.csv"
OUTPUT_DIR = "outputs"

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================================
# STEP 1: LOAD DATA
# ============================================================================

print("[STEP 1/5] LOADING DATA")
print("-" * 80)

tickets_df = pd.read_csv(INPUT_TICKETS)
effort_df = pd.read_csv(INPUT_EFFORT)

print(f"[OK] Loaded {len(tickets_df)} tickets")
print(f"[OK] Loaded {len(effort_df)} effort records")
print()

# ============================================================================
# STEP 2: CLEAN AND TRANSFORM DATA
# ============================================================================

print("[STEP 2/5] CLEANING AND TRANSFORMING DATA")
print("-" * 80)

# Parse dates
tickets_df['created_datetime'] = pd.to_datetime(tickets_df['created_datetime'])
tickets_df['resolved_datetime'] = pd.to_datetime(tickets_df['resolved_datetime'])

# Add time features
tickets_df['year_month'] = tickets_df['created_datetime'].dt.to_period('M')
tickets_df['month_name'] = tickets_df['created_datetime'].dt.strftime('%B %Y')

# Calculate resolution time
tickets_df['resolution_time_hours'] = (
    tickets_df['resolved_datetime'] - tickets_df['created_datetime']
).dt.total_seconds() / 3600

# SLA compliance
tickets_df['sla_met'] = tickets_df['resolution_time_hours'] <= tickets_df['sla_target_hours']
tickets_df.loc[tickets_df['status'].isin(['Open', 'In Progress']), 'sla_met'] = None

# CSAT categories
tickets_df['csat_score_clean'] = tickets_df['csat_score'].fillna(0)
tickets_df['csat_high'] = tickets_df['csat_score'] >= 4
tickets_df['csat_low'] = tickets_df['csat_score'] <= 2
tickets_df['csat_has_score'] = tickets_df['csat_score'].notna()

# Backlog flag
tickets_df['is_backlog'] = tickets_df['status'].isin(['Open', 'In Progress'])
tickets_df['was_reopened'] = tickets_df['reopened_flag'] == 1

print(f"[OK] Parsed {tickets_df['created_datetime'].notna().sum()} dates")
print(f"[OK] Calculated resolution times for {tickets_df['resolution_time_hours'].notna().sum()} tickets")
print(f"[OK] Identified {tickets_df['is_backlog'].sum()} backlog tickets")
print()

# Save master file
tickets_df.to_csv(f"{OUTPUT_DIR}/tickets_master.csv", index=False)
print(f"[OK] Saved: {OUTPUT_DIR}/tickets_master.csv")
print()

# ============================================================================
# STEP 3: CALCULATE KPIs
# ============================================================================

print("[STEP 3/5] CALCULATING KPIs")
print("-" * 80)

# Group by month, hub, function
kpi_groups = tickets_df.groupby(['year_month', 'hub', 'function'])

kpi_summary = pd.DataFrame({
    # Volume metrics
    'total_tickets': kpi_groups.size(),
    'tickets_critical': kpi_groups.apply(lambda x: (x['priority'] == 'Critical').sum(), include_groups=False),
    'tickets_high': kpi_groups.apply(lambda x: (x['priority'] == 'High').sum(), include_groups=False),
    'tickets_medium': kpi_groups.apply(lambda x: (x['priority'] == 'Medium').sum(), include_groups=False),
    'tickets_low': kpi_groups.apply(lambda x: (x['priority'] == 'Low').sum(), include_groups=False),

    # Channel breakdown
    'tickets_email': kpi_groups.apply(lambda x: (x['channel'] == 'Email').sum(), include_groups=False),
    'tickets_portal': kpi_groups.apply(lambda x: (x['channel'] == 'Portal').sum(), include_groups=False),
    'tickets_phone': kpi_groups.apply(lambda x: (x['channel'] == 'Phone').sum(), include_groups=False),
    'tickets_chat': kpi_groups.apply(lambda x: (x['channel'] == 'Chat').sum(), include_groups=False),

    # SLA metrics
    'sla_total_evaluated': kpi_groups.apply(lambda x: x['sla_met'].notna().sum(), include_groups=False),
    'sla_met_count': kpi_groups.apply(lambda x: (x['sla_met'] == True).sum(), include_groups=False),
    'sla_compliance_pct': kpi_groups.apply(
        lambda x: (x['sla_met'] == True).sum() / x['sla_met'].notna().sum() * 100 if x['sla_met'].notna().sum() > 0 else 0,
        include_groups=False
    ),
    'avg_resolution_time_hours': kpi_groups['resolution_time_hours'].mean(),

    # Backlog and reopen
    'backlog_count': kpi_groups['is_backlog'].sum(),
    'reopen_count': kpi_groups['was_reopened'].sum(),
    'reopen_rate_pct': kpi_groups.apply(
        lambda x: x['was_reopened'].sum() / len(x) * 100 if len(x) > 0 else 0,
        include_groups=False
    ),

    # CSAT metrics
    'csat_responses': kpi_groups['csat_has_score'].sum(),
    'csat_avg_score': kpi_groups.apply(
        lambda x: x.loc[x['csat_has_score'], 'csat_score'].mean(),
        include_groups=False
    ),
    'csat_high_count': kpi_groups['csat_high'].sum(),
    'csat_high_pct': kpi_groups.apply(
        lambda x: (x['csat_high']).sum() / x['csat_has_score'].sum() * 100 if x['csat_has_score'].sum() > 0 else 0,
        include_groups=False
    ),
    'csat_low_count': kpi_groups['csat_low'].sum(),
    'csat_low_pct': kpi_groups.apply(
        lambda x: (x['csat_low']).sum() / x['csat_has_score'].sum() * 100 if x['csat_has_score'].sum() > 0 else 0,
        include_groups=False
    ),
}).reset_index()

# Format
kpi_summary['year_month'] = kpi_summary['year_month'].astype(str)
numeric_cols = kpi_summary.select_dtypes(include=['float64']).columns
kpi_summary[numeric_cols] = kpi_summary[numeric_cols].round(2)

# Save KPI summary
kpi_summary.to_csv(f"{OUTPUT_DIR}/kpi_monthly_summary.csv", index=False)

print(f"[OK] Calculated KPIs for {len(kpi_summary)} month/hub/function combinations")
print(f"[OK] Saved: {OUTPUT_DIR}/kpi_monthly_summary.csv")
print()

# ============================================================================
# STEP 4: CALCULATE AGENT PERFORMANCE
# ============================================================================

print("[STEP 4/5] CALCULATING AGENT PERFORMANCE")
print("-" * 80)

# Count tickets per agent per month
tickets_df['month'] = tickets_df['created_datetime'].dt.to_period('M').astype(str)
agent_ticket_counts = tickets_df.groupby(['assigned_agent_id', 'hub', 'function', 'month']).size().reset_index(name='tickets_handled')

# Merge with effort data
agent_performance = effort_df.merge(
    agent_ticket_counts,
    left_on=['agent_id', 'hub', 'function', 'month'],
    right_on=['assigned_agent_id', 'hub', 'function', 'month'],
    how='left'
)

agent_performance['tickets_handled'] = agent_performance['tickets_handled'].fillna(0)
agent_performance['utilization_pct'] = (
    agent_performance['ticket_work_hours'] / agent_performance['total_working_hours'] * 100
).round(2)
agent_performance['avg_hours_per_ticket'] = (
    agent_performance['ticket_work_hours'] / agent_performance['tickets_handled']
).replace([float('inf')], 0).round(2)

# Select columns
agent_performance = agent_performance[[
    'agent_id', 'hub', 'function', 'month',
    'tickets_handled', 'total_working_hours', 'ticket_work_hours',
    'utilization_pct', 'avg_hours_per_ticket'
]]

agent_performance.to_csv(f"{OUTPUT_DIR}/agent_performance.csv", index=False)

print(f"[OK] Calculated metrics for {agent_performance['agent_id'].nunique()} agents")
print(f"[OK] Saved: {OUTPUT_DIR}/agent_performance.csv")
print()

# ============================================================================
# STEP 5: GENERATE SUMMARY REPORT
# ============================================================================

print("[STEP 5/5] GENERATING SUMMARY REPORT")
print("-" * 80)

summary_stats = {
    'Total Tickets': len(tickets_df),
    'Date Range': f"{tickets_df['created_datetime'].min().date()} to {tickets_df['created_datetime'].max().date()}",
    'Hub A Tickets': (tickets_df['hub'] == 'A').sum(),
    'Hub B Tickets': (tickets_df['hub'] == 'B').sum(),
    'Unique Agents': tickets_df['assigned_agent_id'].nunique(),
    'Current Backlog': tickets_df['is_backlog'].sum(),
    'Avg Resolution Time (hrs)': tickets_df['resolution_time_hours'].mean(),
    'Overall SLA Compliance': f"{(tickets_df['sla_met'] == True).sum() / tickets_df['sla_met'].notna().sum() * 100:.1f}%",
    'Avg CSAT Score': f"{tickets_df.loc[tickets_df['csat_has_score'], 'csat_score'].mean():.2f}/5"
}

print()
for key, value in summary_stats.items():
    print(f"  {key:.<40} {value}")

print()
print("=" * 80)
print(" " * 25 + "PROCESSING COMPLETE!")
print("=" * 80)
print()
print("OUTPUT FILES GENERATED:")
print(f"  1. {OUTPUT_DIR}/tickets_master.csv         - Clean ticket data with enrichments")
print(f"  2. {OUTPUT_DIR}/kpi_monthly_summary.csv    - KPI metrics by month/hub/function")
print(f"  3. {OUTPUT_DIR}/agent_performance.csv      - Agent workload and efficiency")
print()
print("NEXT STEPS:")
print("  • Open output files in Excel for analysis")
print("  • Run: streamlit run streamlit_app.py (for interactive dashboard)")
print("  • Review KPI trends and hub comparisons")
print()
print("=" * 80)
print()
