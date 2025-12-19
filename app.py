"""
Support Operations Performance Dashboard
Interactive Streamlit Application with Required Dashboards

Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Support Operations Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #555;
        text-align: center;
        padding-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .highlight-positive {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .highlight-negative {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0 0;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

@st.cache_data
def load_data():
    """Load processed data files"""
    try:
        tickets = pd.read_csv("outputs/tickets_master.csv")
        kpis = pd.read_csv("outputs/kpi_monthly_summary.csv")
        agents = pd.read_csv("outputs/agent_performance.csv")

        # Parse dates
        tickets['created_datetime'] = pd.to_datetime(tickets['created_datetime'])
        tickets['resolved_datetime'] = pd.to_datetime(tickets['resolved_datetime'])

        # Ensure year_month is string for plotting
        tickets['year_month'] = tickets['year_month'].astype(str)

        return tickets, kpis, agents, None
    except FileNotFoundError as e:
        return None, None, None, "Data files not found. Please run main.py first!"
    except Exception as e:
        return None, None, None, f"Error loading data: {str(e)}"

def get_last_month_data(df):
    """Get data for the last complete month"""
    max_month = df['year_month'].max()
    return df[df['year_month'] == max_month]

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    # Header
    st.markdown('<div class="main-header">📊 Support Operations Performance Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">OrionEdge Corp | Hub A (Bangalore) & Hub B (Krakow)</div>', unsafe_allow_html=True)
    st.markdown("---")

    # Load data
    tickets_df, kpis_df, agents_df, error = load_data()

    if error:
        st.error(error)
        st.info("Please run: **python main.py** to generate the data files first.")
        st.stop()

    # ========================================================================
    # SIDEBAR FILTERS
    # ========================================================================

    st.sidebar.header("🔍 Global Filters")

    # Hub filter
    hub_options = ['All'] + sorted(tickets_df['hub'].unique().tolist())
    selected_hub = st.sidebar.selectbox("📍 Hub", hub_options)

    # Function filter
    function_options = ['All'] + sorted(tickets_df['function'].unique().tolist())
    selected_function = st.sidebar.selectbox("💼 Function", function_options)

    # Date range filter
    st.sidebar.subheader("📅 Date Range")
    min_date = tickets_df['created_datetime'].min().date()
    max_date = tickets_df['created_datetime'].max().date()

    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # Apply filters
    filtered_tickets = tickets_df.copy()
    filtered_kpis = kpis_df.copy()

    if selected_hub != 'All':
        filtered_tickets = filtered_tickets[filtered_tickets['hub'] == selected_hub]
        filtered_kpis = filtered_kpis[filtered_kpis['hub'] == selected_hub]

    if selected_function != 'All':
        filtered_tickets = filtered_tickets[filtered_tickets['function'] == selected_function]
        filtered_kpis = filtered_kpis[filtered_kpis['function'] == selected_function]

    if len(date_range) == 2:
        filtered_tickets = filtered_tickets[
            (filtered_tickets['created_datetime'].dt.date >= date_range[0]) &
            (filtered_tickets['created_datetime'].dt.date <= date_range[1])
        ]

    st.sidebar.markdown("---")
    st.sidebar.info(f"📊 Filtered Data: {len(filtered_tickets)} tickets")

    # ========================================================================
    # KEY METRICS OVERVIEW
    # ========================================================================

    st.header("📈 Key Performance Indicators")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        total_tickets = len(filtered_tickets)
        st.metric("🎫 Total Tickets", f"{total_tickets:,}")

    with col2:
        backlog_count = filtered_tickets['is_backlog'].sum()
        backlog_pct = (backlog_count / total_tickets * 100) if total_tickets > 0 else 0
        st.metric("📋 Backlog", f"{backlog_count:,}", f"{backlog_pct:.1f}%")

    with col3:
        resolved = filtered_tickets[filtered_tickets['sla_met'].notna()]
        if len(resolved) > 0:
            sla_pct = (resolved['sla_met'].sum() / len(resolved)) * 100
            st.metric("✅ SLA Compliance", f"{sla_pct:.1f}%")
        else:
            st.metric("✅ SLA Compliance", "N/A")

    with col4:
        with_csat = filtered_tickets[filtered_tickets['csat_has_score']]
        if len(with_csat) > 0:
            avg_csat = with_csat['csat_score'].mean()
            st.metric("⭐ Avg CSAT", f"{avg_csat:.2f}/5")
        else:
            st.metric("⭐ Avg CSAT", "N/A")

    with col5:
        resolved_tickets = filtered_tickets[filtered_tickets['resolution_time_hours'].notna()]
        if len(resolved_tickets) > 0:
            avg_resolution = resolved_tickets['resolution_time_hours'].mean()
            st.metric("⏱️ Avg Resolution", f"{avg_resolution:.1f}h")
        else:
            st.metric("⏱️ Avg Resolution", "N/A")

    st.markdown("---")

    # ========================================================================
    # TAB NAVIGATION - REQUIRED DASHBOARDS
    # ========================================================================

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Volume & Distribution",
        "⏱️ SLA & Resolution Performance",
        "⭐ CSAT Analysis",
        "📋 Management Summary",
        "📈 Detailed KPI Table"
    ])

    # ========================================================================
    # TAB 1: VOLUME & DISTRIBUTION VIEW
    # ========================================================================

    with tab1:
        st.header("📊 Volume & Distribution View")
        st.markdown("**Analyze ticket volumes and distribution patterns**")
        st.markdown("---")

        # Trend of ticket volumes by month
        st.subheader("📈 Ticket Volume Trend by Month")

        monthly_volume = filtered_tickets.groupby(['year_month', 'hub']).size().reset_index(name='ticket_count')

        fig = px.line(
            monthly_volume,
            x='year_month',
            y='ticket_count',
            color='hub',
            markers=True,
            labels={'year_month': 'Month', 'ticket_count': 'Number of Tickets', 'hub': 'Hub'},
            color_discrete_map={'A': '#1f77b4', 'B': '#ff7f0e'},
            title="Monthly Ticket Trend by Hub"
        )
        fig.update_layout(height=400, hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # Breakdown by hub, function, category, channel
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🏢 Breakdown by Hub")
            hub_dist = filtered_tickets['hub'].value_counts()

            fig = px.pie(
                values=hub_dist.values,
                names=hub_dist.index,
                title="Ticket Distribution by Hub",
                hole=0.4,
                color_discrete_sequence=['#1f77b4', '#ff7f0e']
            )
            fig.update_traces(textposition='inside', textinfo='percent+label+value')
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("💼 Breakdown by Function")
            func_dist = filtered_tickets['function'].value_counts()

            fig = px.pie(
                values=func_dist.values,
                names=func_dist.index,
                title="Ticket Distribution by Function",
                hole=0.4,
                color_discrete_sequence=['#2ca02c', '#d62728', '#9467bd']
            )
            fig.update_traces(textposition='inside', textinfo='percent+label+value')
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📂 Top 10 Categories")
            top_categories = filtered_tickets['category'].value_counts().head(10)

            fig = px.bar(
                y=top_categories.index,
                x=top_categories.values,
                orientation='h',
                labels={'x': 'Number of Tickets', 'y': 'Category'},
                title="Most Common Issue Categories",
                color=top_categories.values,
                color_continuous_scale='Blues'
            )
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("📞 Distribution by Channel")
            channel_dist = filtered_tickets['channel'].value_counts()

            fig = px.bar(
                x=channel_dist.index,
                y=channel_dist.values,
                labels={'x': 'Channel', 'y': 'Number of Tickets'},
                title="Tickets by Communication Channel",
                color=channel_dist.index,
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # Priority breakdown
        st.subheader("🚨 Ticket Priority Distribution")
        priority_by_month = filtered_tickets.groupby(['year_month', 'priority']).size().reset_index(name='count')

        fig = px.bar(
            priority_by_month,
            x='year_month',
            y='count',
            color='priority',
            labels={'year_month': 'Month', 'count': 'Number of Tickets'},
            title="Ticket Priority Distribution Over Time",
            color_discrete_map={
                'Critical': '#d62728',
                'High': '#ff7f0e',
                'Medium': '#1f77b4',
                'Low': '#2ca02c'
            }
        )
        fig.update_layout(height=400, barmode='stack')
        st.plotly_chart(fig, use_container_width=True)

    # ========================================================================
    # TAB 2: SLA & RESOLUTION PERFORMANCE VIEW
    # ========================================================================

    with tab2:
        st.header("⏱️ SLA & Resolution Performance View")
        st.markdown("**Monitor SLA compliance and resolution efficiency**")
        st.markdown("---")

        # SLA % and Avg Resolution Time trend
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("✅ SLA Compliance Trend")
            sla_trend = filtered_kpis.groupby('year_month').agg({
                'sla_compliance_pct': 'mean'
            }).reset_index()

            fig = px.line(
                sla_trend,
                x='year_month',
                y='sla_compliance_pct',
                markers=True,
                labels={'year_month': 'Month', 'sla_compliance_pct': 'SLA Compliance %'},
                title="SLA Compliance % Over Time"
            )
            fig.add_hline(y=80, line_dash="dash", line_color="green",
                         annotation_text="Target: 80%", annotation_position="right")
            fig.update_layout(height=350)
            fig.update_traces(line_color='#1f77b4', line_width=3)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("⏱️ Avg Resolution Time Trend")
            resolution_trend = filtered_kpis.groupby('year_month').agg({
                'avg_resolution_time_hours': 'mean'
            }).reset_index()

            fig = px.line(
                resolution_trend,
                x='year_month',
                y='avg_resolution_time_hours',
                markers=True,
                labels={'year_month': 'Month', 'avg_resolution_time_hours': 'Avg Resolution Time (hours)'},
                title="Average Resolution Time Over Time"
            )
            fig.update_layout(height=350)
            fig.update_traces(line_color='#ff7f0e', line_width=3)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # Hub A vs Hub B Comparison
        st.subheader("🏢 Hub A vs Hub B Comparison")

        if selected_hub == 'All':
            hub_comparison = filtered_kpis.groupby('hub').agg({
                'sla_compliance_pct': 'mean',
                'avg_resolution_time_hours': 'mean',
                'total_tickets': 'sum'
            }).round(2).reset_index()

            col1, col2, col3 = st.columns(3)

            with col1:
                fig = go.Figure(data=[
                    go.Bar(name='Hub A', x=['SLA %'], y=[hub_comparison[hub_comparison['hub']=='A']['sla_compliance_pct'].values[0]], marker_color='#1f77b4'),
                    go.Bar(name='Hub B', x=['SLA %'], y=[hub_comparison[hub_comparison['hub']=='B']['sla_compliance_pct'].values[0]], marker_color='#ff7f0e')
                ])
                fig.update_layout(title="SLA Compliance Comparison", height=300, showlegend=True)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig = go.Figure(data=[
                    go.Bar(name='Hub A', x=['Resolution Time'], y=[hub_comparison[hub_comparison['hub']=='A']['avg_resolution_time_hours'].values[0]], marker_color='#1f77b4'),
                    go.Bar(name='Hub B', x=['Resolution Time'], y=[hub_comparison[hub_comparison['hub']=='B']['avg_resolution_time_hours'].values[0]], marker_color='#ff7f0e')
                ])
                fig.update_layout(title="Avg Resolution Time (hours)", height=300, showlegend=True)
                st.plotly_chart(fig, use_container_width=True)

            with col3:
                fig = go.Figure(data=[
                    go.Bar(name='Hub A', x=['Tickets'], y=[hub_comparison[hub_comparison['hub']=='A']['total_tickets'].values[0]], marker_color='#1f77b4'),
                    go.Bar(name='Hub B', x=['Tickets'], y=[hub_comparison[hub_comparison['hub']=='B']['total_tickets'].values[0]], marker_color='#ff7f0e')
                ])
                fig.update_layout(title="Total Tickets Processed", height=300, showlegend=True)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(f"Viewing data for Hub {selected_hub} only. Select 'All' in sidebar to see hub comparison.")

        st.markdown("---")

        # Top 5 categories with worst SLA % or highest resolution time
        st.subheader("🔴 Top 5 Categories with Worst SLA Performance")

        resolved_tickets = filtered_tickets[filtered_tickets['sla_met'].notna()].copy()
        category_sla = resolved_tickets.groupby('category').agg({
            'sla_met': lambda x: (x.sum() / len(x) * 100),
            'resolution_time_hours': 'mean',
            'ticket_id': 'count'
        }).round(2)
        category_sla.columns = ['SLA Compliance %', 'Avg Resolution Time (hrs)', 'Ticket Count']
        category_sla = category_sla[category_sla['Ticket Count'] >= 3]  # Only categories with 3+ tickets
        worst_sla = category_sla.nsmallest(5, 'SLA Compliance %')

        col1, col2 = st.columns(2)

        with col1:
            fig = px.bar(
                x=worst_sla['SLA Compliance %'],
                y=worst_sla.index,
                orientation='h',
                labels={'x': 'SLA Compliance %', 'y': 'Category'},
                title="5 Categories with Lowest SLA Compliance",
                color=worst_sla['SLA Compliance %'],
                color_continuous_scale='Reds_r'
            )
            fig.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            highest_resolution = category_sla.nlargest(5, 'Avg Resolution Time (hrs)')

            fig = px.bar(
                x=highest_resolution['Avg Resolution Time (hrs)'],
                y=highest_resolution.index,
                orientation='h',
                labels={'x': 'Avg Resolution Time (hours)', 'y': 'Category'},
                title="5 Categories with Highest Resolution Time",
                color=highest_resolution['Avg Resolution Time (hrs)'],
                color_continuous_scale='Oranges'
            )
            fig.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        # Detailed table
        st.subheader("📊 Category Performance Details")
        st.dataframe(
            category_sla.sort_values('SLA Compliance %'),
            use_container_width=True,
            height=300
        )

    # ========================================================================
    # TAB 3: CSAT VIEW
    # ========================================================================

    with tab3:
        st.header("⭐ CSAT (Customer Satisfaction) Analysis")
        st.markdown("**Monitor customer satisfaction trends and patterns**")
        st.markdown("---")

        # Filter for tickets with CSAT scores
        csat_tickets = filtered_tickets[filtered_tickets['csat_has_score']].copy()

        if len(csat_tickets) == 0:
            st.warning("No CSAT data available for the selected filters.")
        else:
            # Avg CSAT per hub and per function
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("🏢 Average CSAT by Hub")
                csat_by_hub = csat_tickets.groupby('hub')['csat_score'].mean().round(2)

                fig = go.Figure(data=[
                    go.Bar(
                        x=csat_by_hub.index,
                        y=csat_by_hub.values,
                        text=csat_by_hub.values,
                        textposition='auto',
                        marker_color=['#1f77b4', '#ff7f0e']
                    )
                ])
                fig.update_layout(
                    title="Average CSAT Score by Hub",
                    yaxis_range=[0, 5],
                    yaxis_title="CSAT Score (out of 5)",
                    xaxis_title="Hub",
                    height=350
                )
                fig.add_hline(y=4, line_dash="dash", line_color="green",
                             annotation_text="Target: 4.0", annotation_position="right")
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.subheader("💼 Average CSAT by Function")
                csat_by_function = csat_tickets.groupby('function')['csat_score'].mean().round(2)

                fig = go.Figure(data=[
                    go.Bar(
                        x=csat_by_function.index,
                        y=csat_by_function.values,
                        text=csat_by_function.values,
                        textposition='auto',
                        marker_color=['#2ca02c', '#d62728', '#9467bd']
                    )
                ])
                fig.update_layout(
                    title="Average CSAT Score by Function",
                    yaxis_range=[0, 5],
                    yaxis_title="CSAT Score (out of 5)",
                    xaxis_title="Function",
                    height=350
                )
                fig.add_hline(y=4, line_dash="dash", line_color="green",
                             annotation_text="Target: 4.0", annotation_position="right")
                st.plotly_chart(fig, use_container_width=True)

            st.markdown("---")

            # Trend of CSAT over months
            st.subheader("📈 CSAT Trend Over Time")

            csat_trend = csat_tickets.groupby(['year_month', 'hub']).agg({
                'csat_score': 'mean'
            }).reset_index()

            fig = px.line(
                csat_trend,
                x='year_month',
                y='csat_score',
                color='hub',
                markers=True,
                labels={'year_month': 'Month', 'csat_score': 'Average CSAT Score', 'hub': 'Hub'},
                title="CSAT Score Trend by Hub",
                color_discrete_map={'A': '#1f77b4', 'B': '#ff7f0e'}
            )
            fig.add_hline(y=4, line_dash="dash", line_color="green",
                         annotation_text="Target: 4.0", annotation_position="right")
            fig.update_layout(height=400, yaxis_range=[0, 5], hovermode='x unified')
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("---")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📊 CSAT Score Distribution")
                csat_dist = csat_tickets['csat_score'].value_counts().sort_index()

                fig = px.bar(
                    x=csat_dist.index,
                    y=csat_dist.values,
                    labels={'x': 'CSAT Score', 'y': 'Number of Responses'},
                    title="Distribution of CSAT Scores",
                    color=csat_dist.values,
                    color_continuous_scale='RdYlGn'
                )
                fig.update_layout(height=350, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.subheader("🎯 CSAT Categories")

                high_csat = (csat_tickets['csat_score'] >= 4).sum()
                medium_csat = ((csat_tickets['csat_score'] == 3)).sum()
                low_csat = (csat_tickets['csat_score'] <= 2).sum()

                fig = go.Figure(data=[go.Pie(
                    labels=['High (4-5)', 'Medium (3)', 'Low (1-2)'],
                    values=[high_csat, medium_csat, low_csat],
                    marker_colors=['#2ca02c', '#ffcc00', '#d62728'],
                    hole=0.4
                )])
                fig.update_layout(title="CSAT Score Categories", height=350)
                fig.update_traces(textposition='inside', textinfo='percent+label+value')
                st.plotly_chart(fig, use_container_width=True)

            # CSAT by category
            st.subheader("📂 CSAT by Category (Top 10)")
            csat_by_category = csat_tickets.groupby('category').agg({
                'csat_score': ['mean', 'count']
            }).round(2)
            csat_by_category.columns = ['Avg CSAT', 'Response Count']
            csat_by_category = csat_by_category[csat_by_category['Response Count'] >= 3]
            top_10_categories = csat_by_category.nlargest(10, 'Avg CSAT')

            fig = px.bar(
                y=top_10_categories.index,
                x=top_10_categories['Avg CSAT'],
                orientation='h',
                labels={'x': 'Average CSAT Score', 'y': 'Category'},
                title="Top 10 Categories by CSAT Score",
                color=top_10_categories['Avg CSAT'],
                color_continuous_scale='RdYlGn'
            )
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

    # ========================================================================
    # TAB 4: MANAGEMENT SUMMARY REPORT
    # ========================================================================

    with tab4:
        st.header("📋 Management Summary Report")
        st.markdown("**Executive summary and key insights**")
        st.markdown("---")

        # Get last month data
        last_month = filtered_tickets['year_month'].max()
        last_month_tickets = filtered_tickets[filtered_tickets['year_month'] == last_month]

        st.subheader(f"📅 Summary for: {last_month}")

        # Key KPIs for last month
        st.markdown("### 🎯 Key KPIs (Last Month)")

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            total = len(last_month_tickets)
            st.metric("Total Tickets", f"{total}")

        with col2:
            backlog = last_month_tickets['is_backlog'].sum()
            st.metric("Backlog", f"{backlog}", f"{backlog/total*100:.1f}%" if total > 0 else "0%")

        with col3:
            resolved = last_month_tickets[last_month_tickets['sla_met'].notna()]
            sla = (resolved['sla_met'].sum() / len(resolved) * 100) if len(resolved) > 0 else 0
            st.metric("SLA Compliance", f"{sla:.1f}%")

        with col4:
            with_csat = last_month_tickets[last_month_tickets['csat_has_score']]
            avg_csat = with_csat['csat_score'].mean() if len(with_csat) > 0 else 0
            st.metric("Avg CSAT", f"{avg_csat:.2f}/5")

        with col5:
            resolved_tickets = last_month_tickets[last_month_tickets['resolution_time_hours'].notna()]
            avg_res = resolved_tickets['resolution_time_hours'].mean() if len(resolved_tickets) > 0 else 0
            st.metric("Avg Resolution", f"{avg_res:.1f}h")

        st.markdown("---")

        # Two columns for improvements and highlights
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🔴 Top 3 Improvement Areas")

            improvements = []

            # 1. Check SLA compliance
            if sla < 80:
                improvements.append({
                    'area': '⏱️ SLA Compliance Below Target',
                    'current': f'{sla:.1f}%',
                    'target': '80%',
                    'detail': f'Current SLA compliance is {80-sla:.1f}% below target. Focus on reducing resolution times.'
                })

            # 2. Check backlog
            backlog_pct = (backlog/total*100) if total > 0 else 0
            if backlog_pct > 30:
                improvements.append({
                    'area': '📋 High Backlog',
                    'current': f'{backlog} tickets ({backlog_pct:.1f}%)',
                    'target': '<30%',
                    'detail': 'Significant backlog accumulation. Consider resource allocation or process optimization.'
                })

            # 3. Check CSAT
            if avg_csat < 4.0:
                improvements.append({
                    'area': '⭐ Customer Satisfaction Below Target',
                    'current': f'{avg_csat:.2f}/5',
                    'target': '4.0/5',
                    'detail': 'CSAT score needs improvement. Review customer feedback and service quality.'
                })

            # 4. Check resolution time
            if avg_res > 24:
                improvements.append({
                    'area': '⏰ High Resolution Time',
                    'current': f'{avg_res:.1f} hours',
                    'target': '<24 hours',
                    'detail': 'Average resolution time exceeds target. Identify bottlenecks in the process.'
                })

            # 5. Check worst categories
            if len(last_month_tickets) > 0:
                worst_category = last_month_tickets['category'].value_counts().idxmax()
                worst_count = last_month_tickets['category'].value_counts().max()
                if worst_count > len(last_month_tickets) * 0.15:
                    improvements.append({
                        'area': f'📂 High Volume Category: {worst_category}',
                        'current': f'{worst_count} tickets ({worst_count/len(last_month_tickets)*100:.1f}%)',
                        'target': '<15% per category',
                        'detail': f'{worst_category} represents unusually high volume. Investigate root causes.'
                    })

            # Display top 3
            for i, imp in enumerate(improvements[:3], 1):
                st.markdown(f"""
                <div class="highlight-negative">
                    <strong>{i}. {imp['area']}</strong><br>
                    Current: {imp['current']} | Target: {imp['target']}<br>
                    <em>{imp['detail']}</em>
                </div>
                """, unsafe_allow_html=True)

            if len(improvements) == 0:
                st.success("✅ All metrics are meeting targets! Great performance!")

        with col2:
            st.markdown("### 🟢 Top 3 Positive Highlights")

            highlights = []

            # 1. High SLA compliance
            if sla >= 80:
                highlights.append({
                    'area': '✅ Excellent SLA Compliance',
                    'value': f'{sla:.1f}%',
                    'detail': f'SLA compliance is {sla-80:.1f}% above target. Maintaining excellent service levels.'
                })

            # 2. High CSAT
            if avg_csat >= 4.0:
                highlights.append({
                    'area': '⭐ High Customer Satisfaction',
                    'value': f'{avg_csat:.2f}/5',
                    'detail': 'CSAT scores are meeting or exceeding targets. Customers are satisfied with service.'
                })

            # 3. Low backlog
            if backlog_pct < 20:
                highlights.append({
                    'area': '📋 Manageable Backlog',
                    'value': f'{backlog_pct:.1f}%',
                    'detail': 'Backlog is well-controlled. Efficient ticket processing and resource allocation.'
                })

            # 4. Quick resolution
            if avg_res < 24:
                highlights.append({
                    'area': '⚡ Fast Resolution Times',
                    'value': f'{avg_res:.1f} hours',
                    'detail': 'Average resolution time is below 24 hours. Efficient problem-solving process.'
                })

            # 5. Volume handling
            prev_month = filtered_tickets['year_month'].unique()
            if len(prev_month) >= 2:
                prev_month_sorted = sorted(prev_month)
                if len(prev_month_sorted) >= 2:
                    prev = prev_month_sorted[-2]
                    prev_total = len(filtered_tickets[filtered_tickets['year_month'] == prev])
                    if total > prev_total:
                        growth = ((total - prev_total) / prev_total * 100)
                        highlights.append({
                            'area': f'📈 Volume Handled ({growth:.1f}% increase)',
                            'value': f'{total} tickets',
                            'detail': f'Successfully handled {growth:.1f}% more tickets compared to previous month.'
                        })

            # 6. Best performing hub/function
            if selected_hub == 'All':
                hub_sla = last_month_tickets.groupby('hub').apply(
                    lambda x: (x['sla_met'].sum() / x['sla_met'].notna().sum() * 100) if x['sla_met'].notna().sum() > 0 else 0
                )
                if len(hub_sla) > 0:
                    best_hub = hub_sla.idxmax()
                    best_sla = hub_sla.max()
                    if best_sla >= 50:
                        highlights.append({
                            'area': f'🏆 Best Performing Hub: Hub {best_hub}',
                            'value': f'{best_sla:.1f}% SLA',
                            'detail': f'Hub {best_hub} is outperforming with highest SLA compliance.'
                        })

            # Display top 3
            for i, highlight in enumerate(highlights[:3], 1):
                st.markdown(f"""
                <div class="highlight-positive">
                    <strong>{i}. {highlight['area']}</strong><br>
                    Value: {highlight['value']}<br>
                    <em>{highlight['detail']}</em>
                </div>
                """, unsafe_allow_html=True)

            if len(highlights) == 0:
                st.info("Continue monitoring metrics to identify positive trends.")

        st.markdown("---")

        # Additional insights
        st.markdown("### 📊 Additional Insights")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🏆 Top Performing Categories (by SLA)")
            resolved_last_month = last_month_tickets[last_month_tickets['sla_met'].notna()]
            if len(resolved_last_month) > 0:
                cat_sla = resolved_last_month.groupby('category').apply(
                    lambda x: (x['sla_met'].sum() / len(x) * 100)
                ).round(2).sort_values(ascending=False).head(5)

                for cat, sla_val in cat_sla.items():
                    st.write(f"• **{cat}**: {sla_val:.1f}% SLA")
            else:
                st.info("No SLA data available for last month.")

        with col2:
            st.markdown("#### 👥 Top Performing Agents")
            if agents_df is not None:
                last_month_str = str(last_month)
                agents_last_month = agents_df[agents_df['month'] == last_month_str]

                if len(agents_last_month) > 0:
                    top_agents = agents_last_month.nlargest(5, 'tickets_handled')[['agent_id', 'tickets_handled', 'utilization_pct']]

                    for _, agent in top_agents.iterrows():
                        st.write(f"• **{agent['agent_id']}**: {int(agent['tickets_handled'])} tickets ({agent['utilization_pct']:.1f}% util)")
                else:
                    st.info("No agent data available for last month.")

        st.markdown("---")

        # Action Items
        st.markdown("### 🎯 Recommended Action Items")

        action_items = []

        if sla < 80:
            action_items.append("• **Improve SLA Compliance**: Analyze bottlenecks in ticket resolution process")

        if backlog_pct > 30:
            action_items.append("• **Address Backlog**: Allocate additional resources or optimize workflows")

        if avg_csat < 4.0:
            action_items.append("• **Enhance Customer Satisfaction**: Review feedback and improve service quality")

        if len(improvements) > 0:
            worst_cat = improvements[0]['area']
            action_items.append(f"• **Focus on**: {worst_cat}")

        action_items.append("• **Regular Monitoring**: Continue tracking KPIs weekly")
        action_items.append("• **Knowledge Sharing**: Share best practices from high-performing hubs/agents")

        for item in action_items:
            st.markdown(item)

        # Export button
        st.markdown("---")
        st.markdown("### 📥 Export Report Data")

        report_data = {
            'Month': [last_month],
            'Total Tickets': [total],
            'Backlog': [backlog],
            'SLA Compliance %': [f"{sla:.1f}"],
            'Avg CSAT': [f"{avg_csat:.2f}"],
            'Avg Resolution Hours': [f"{avg_res:.1f}"]
        }
        report_df = pd.DataFrame(report_data)

        csv = report_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Management Summary (CSV)",
            data=csv,
            file_name=f'management_summary_{last_month}.csv',
            mime='text/csv'
        )

    # ========================================================================
    # TAB 5: DETAILED KPI TABLE
    # ========================================================================

    with tab5:
        st.header("📈 Detailed KPI Table")
        st.markdown("**Comprehensive KPI metrics for each Month / Hub / Function**")
        st.markdown("---")

        # Display full KPI summary table
        st.subheader("📊 Core KPIs by Month, Hub & Function")

        # Create a formatted display of KPIs
        display_kpis = filtered_kpis.copy()

        # Select and rename columns for display
        kpi_display_columns = {
            'year_month': 'Month',
            'hub': 'Hub',
            'function': 'Function',
            'total_tickets': 'Total Tickets',
            'tickets_critical': 'Critical',
            'tickets_high': 'High',
            'tickets_medium': 'Medium',
            'tickets_low': 'Low',
            'tickets_email': 'Email',
            'tickets_portal': 'Portal',
            'tickets_phone': 'Phone',
            'tickets_chat': 'Chat',
            'sla_compliance_pct': 'SLA Compliance %',
            'avg_resolution_time_hours': 'Avg Resolution (hrs)',
            'backlog_count': 'Backlog',
            'reopen_rate_pct': 'Reopen Rate %',
            'csat_avg_score': 'Avg CSAT',
            'csat_responses': 'CSAT Responses'
        }

        display_kpis = display_kpis[list(kpi_display_columns.keys())].rename(columns=kpi_display_columns)

        # Show interactive dataframe
        st.dataframe(
            display_kpis,
            use_container_width=True,
            height=500
        )

        # Download button
        csv = display_kpis.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Complete KPI Table (CSV)",
            data=csv,
            file_name=f'detailed_kpis_{datetime.now().strftime("%Y%m%d")}.csv',
            mime='text/csv'
        )

        st.markdown("---")

        # Breakdown sections
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Ticket Volume Breakdown")
            st.markdown("**By Channel:**")

            # Channel summary
            channel_summary = filtered_kpis.groupby('year_month').agg({
                'tickets_email': 'sum',
                'tickets_portal': 'sum',
                'tickets_phone': 'sum',
                'tickets_chat': 'sum'
            }).round(0)

            st.dataframe(channel_summary, use_container_width=True)

            st.markdown("**By Priority:**")

            # Priority summary
            priority_summary = filtered_kpis.groupby('year_month').agg({
                'tickets_critical': 'sum',
                'tickets_high': 'sum',
                'tickets_medium': 'sum',
                'tickets_low': 'sum'
            }).round(0)

            st.dataframe(priority_summary, use_container_width=True)

        with col2:
            st.subheader("⏱️ SLA & Resolution Metrics")
            st.markdown("**Monthly Performance:**")

            # SLA and resolution summary
            performance_summary = filtered_kpis.groupby('year_month').agg({
                'sla_compliance_pct': 'mean',
                'avg_resolution_time_hours': 'mean',
                'backlog_count': 'sum',
                'reopen_rate_pct': 'mean'
            }).round(2)

            performance_summary.columns = ['SLA Compliance %', 'Avg Resolution (hrs)', 'Total Backlog', 'Reopen Rate %']

            st.dataframe(performance_summary, use_container_width=True)

            st.markdown("**CSAT Metrics:**")

            # CSAT summary
            csat_summary = filtered_kpis.groupby('year_month').agg({
                'csat_avg_score': 'mean',
                'csat_responses': 'sum',
                'csat_high_pct': 'mean',
                'csat_low_pct': 'mean'
            }).round(2)

            csat_summary.columns = ['Avg CSAT', 'Total Responses', 'High CSAT %', 'Low CSAT %']

            st.dataframe(csat_summary, use_container_width=True)

        st.markdown("---")

        # Hub-wise comparison table
        st.subheader("🏢 Hub-Wise KPI Comparison")

        if selected_hub == 'All':
            hub_comparison_detailed = filtered_kpis.groupby('hub').agg({
                'total_tickets': 'sum',
                'sla_compliance_pct': 'mean',
                'avg_resolution_time_hours': 'mean',
                'backlog_count': 'sum',
                'reopen_rate_pct': 'mean',
                'csat_avg_score': 'mean',
                'tickets_critical': 'sum',
                'tickets_high': 'sum',
                'tickets_medium': 'sum',
                'tickets_low': 'sum'
            }).round(2)

            hub_comparison_detailed.columns = [
                'Total Tickets', 'SLA %', 'Avg Resolution (hrs)',
                'Backlog', 'Reopen %', 'CSAT',
                'Critical', 'High', 'Medium', 'Low'
            ]

            st.dataframe(hub_comparison_detailed, use_container_width=True)

            # Visualize hub comparison
            col1, col2 = st.columns(2)

            with col1:
                fig = go.Figure(data=[
                    go.Bar(
                        name='Hub A',
                        x=['Total Tickets', 'SLA %', 'CSAT'],
                        y=[
                            hub_comparison_detailed.loc['A', 'Total Tickets'],
                            hub_comparison_detailed.loc['A', 'SLA %'],
                            hub_comparison_detailed.loc['A', 'CSAT'] * 20  # Scale to 100
                        ],
                        marker_color='#1f77b4'
                    ),
                    go.Bar(
                        name='Hub B',
                        x=['Total Tickets', 'SLA %', 'CSAT'],
                        y=[
                            hub_comparison_detailed.loc['B', 'Total Tickets'],
                            hub_comparison_detailed.loc['B', 'SLA %'],
                            hub_comparison_detailed.loc['B', 'CSAT'] * 20  # Scale to 100
                        ],
                        marker_color='#ff7f0e'
                    )
                ])
                fig.update_layout(
                    title="Key Metrics Comparison",
                    barmode='group',
                    height=350
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Priority distribution by hub
                priority_data = pd.DataFrame({
                    'Hub A': [
                        hub_comparison_detailed.loc['A', 'Critical'],
                        hub_comparison_detailed.loc['A', 'High'],
                        hub_comparison_detailed.loc['A', 'Medium'],
                        hub_comparison_detailed.loc['A', 'Low']
                    ],
                    'Hub B': [
                        hub_comparison_detailed.loc['B', 'Critical'],
                        hub_comparison_detailed.loc['B', 'High'],
                        hub_comparison_detailed.loc['B', 'Medium'],
                        hub_comparison_detailed.loc['B', 'Low']
                    ]
                }, index=['Critical', 'High', 'Medium', 'Low'])

                fig = go.Figure(data=[
                    go.Bar(name='Hub A', x=priority_data.index, y=priority_data['Hub A'], marker_color='#1f77b4'),
                    go.Bar(name='Hub B', x=priority_data.index, y=priority_data['Hub B'], marker_color='#ff7f0e')
                ])
                fig.update_layout(
                    title="Priority Distribution by Hub",
                    barmode='group',
                    height=350
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(f"Viewing data for Hub {selected_hub} only. Select 'All' in sidebar to see hub comparison.")

        st.markdown("---")

        # Function-wise comparison table
        st.subheader("💼 Function-Wise KPI Comparison")

        if selected_function == 'All':
            function_comparison = filtered_kpis.groupby('function').agg({
                'total_tickets': 'sum',
                'sla_compliance_pct': 'mean',
                'avg_resolution_time_hours': 'mean',
                'backlog_count': 'sum',
                'reopen_rate_pct': 'mean',
                'csat_avg_score': 'mean'
            }).round(2)

            function_comparison.columns = [
                'Total Tickets', 'SLA %', 'Avg Resolution (hrs)',
                'Backlog', 'Reopen %', 'CSAT'
            ]

            st.dataframe(function_comparison, use_container_width=True)

            # Visualize function comparison
            fig = go.Figure(data=[
                go.Bar(
                    x=function_comparison.index,
                    y=function_comparison['Total Tickets'],
                    name='Total Tickets',
                    marker_color='#1f77b4'
                )
            ])
            fig.update_layout(
                title="Total Tickets by Function",
                xaxis_title="Function",
                yaxis_title="Number of Tickets",
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(f"Viewing data for {selected_function} function only. Select 'All' in sidebar to see function comparison.")

        st.markdown("---")

        # Month-over-month trends
        st.subheader("📈 Month-over-Month Trends")

        monthly_trends = filtered_kpis.groupby('year_month').agg({
            'total_tickets': 'sum',
            'sla_compliance_pct': 'mean',
            'avg_resolution_time_hours': 'mean',
            'csat_avg_score': 'mean'
        }).round(2)

        monthly_trends.columns = ['Total Tickets', 'SLA %', 'Avg Resolution (hrs)', 'Avg CSAT']

        # Calculate month-over-month changes
        if len(monthly_trends) > 1:
            monthly_trends['Ticket Change'] = monthly_trends['Total Tickets'].diff()
            monthly_trends['SLA Change'] = monthly_trends['SLA %'].diff()
            monthly_trends['CSAT Change'] = monthly_trends['Avg CSAT'].diff()

        st.dataframe(monthly_trends, use_container_width=True)

        # Trend visualization
        col1, col2 = st.columns(2)

        with col1:
            fig = px.line(
                monthly_trends.reset_index(),
                x='year_month',
                y='SLA %',
                markers=True,
                title="SLA Compliance Trend",
                labels={'year_month': 'Month'}
            )
            fig.add_hline(y=80, line_dash="dash", line_color="green", annotation_text="Target: 80%")
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.line(
                monthly_trends.reset_index(),
                x='year_month',
                y='Avg CSAT',
                markers=True,
                title="CSAT Score Trend",
                labels={'year_month': 'Month'}
            )
            fig.add_hline(y=4, line_dash="dash", line_color="green", annotation_text="Target: 4.0")
            fig.update_layout(height=300, yaxis_range=[0, 5])
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # Agent Metrics Section
        st.subheader("👥 Agent Metrics")
        st.markdown("**Tickets per Agent and Work Utilization**")

        if agents_df is not None and len(agents_df) > 0:
            # Filter agents based on sidebar selections
            filtered_agents = agents_df.copy()

            if selected_hub != 'All':
                filtered_agents = filtered_agents[filtered_agents['hub'] == selected_hub]

            if selected_function != 'All':
                filtered_agents = filtered_agents[filtered_agents['function'] == selected_function]

            # Agent KPI Table
            st.markdown("**📊 Agent Performance by Month:**")

            agent_kpi_display = filtered_agents[[
                'month', 'agent_id', 'hub', 'function',
                'tickets_handled', 'total_working_hours', 'ticket_work_hours',
                'utilization_pct', 'avg_hours_per_ticket'
            ]].copy()

            agent_kpi_display.columns = [
                'Month', 'Agent ID', 'Hub', 'Function',
                'Tickets Handled', 'Total Hours', 'Ticket Work Hours',
                'Utilization %', 'Avg Hours/Ticket'
            ]

            st.dataframe(agent_kpi_display, use_container_width=True, height=400)

            # Download button for agent metrics
            agent_csv = agent_kpi_display.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Agent Metrics (CSV)",
                data=agent_csv,
                file_name=f'agent_metrics_{datetime.now().strftime("%Y%m%d")}.csv',
                mime='text/csv'
            )

            st.markdown("---")

            # Agent Summary Statistics
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**📊 Tickets per Agent (Monthly Average):**")

                agent_monthly_avg = filtered_agents.groupby('agent_id').agg({
                    'tickets_handled': 'mean',
                    'hub': 'first',
                    'function': 'first'
                }).round(2).sort_values('tickets_handled', ascending=False)

                agent_monthly_avg.columns = ['Avg Tickets/Month', 'Hub', 'Function']

                st.dataframe(agent_monthly_avg, use_container_width=True)

                # Visualization
                fig = px.bar(
                    x=agent_monthly_avg.index,
                    y=agent_monthly_avg['Avg Tickets/Month'],
                    labels={'x': 'Agent ID', 'y': 'Average Tickets per Month'},
                    title="Average Tickets Handled per Agent per Month",
                    color=agent_monthly_avg['Avg Tickets/Month'],
                    color_continuous_scale='Blues'
                )
                fig.update_layout(height=350, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.markdown("**⚡ Ticket Work Utilization %:**")

                agent_util_avg = filtered_agents.groupby('agent_id').agg({
                    'utilization_pct': 'mean',
                    'hub': 'first',
                    'function': 'first'
                }).round(2).sort_values('utilization_pct', ascending=False)

                agent_util_avg.columns = ['Avg Utilization %', 'Hub', 'Function']

                st.dataframe(agent_util_avg, use_container_width=True)

                # Visualization
                fig = px.bar(
                    x=agent_util_avg.index,
                    y=agent_util_avg['Avg Utilization %'],
                    labels={'x': 'Agent ID', 'y': 'Average Utilization %'},
                    title="Average Work Utilization % per Agent",
                    color=agent_util_avg['Avg Utilization %'],
                    color_continuous_scale='Oranges'
                )
                fig.add_hline(y=100, line_dash="dash", line_color="red",
                             annotation_text="100% Capacity", annotation_position="right")
                fig.update_layout(height=350, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)

            st.markdown("---")

            # Monthly trend for agents
            st.markdown("**📈 Agent Performance Trends:**")

            col1, col2 = st.columns(2)

            with col1:
                # Tickets handled trend
                agent_monthly_trend = filtered_agents.groupby(['month', 'agent_id']).agg({
                    'tickets_handled': 'sum'
                }).reset_index()

                fig = px.line(
                    agent_monthly_trend,
                    x='month',
                    y='tickets_handled',
                    color='agent_id',
                    markers=True,
                    labels={'month': 'Month', 'tickets_handled': 'Tickets Handled', 'agent_id': 'Agent'},
                    title="Tickets Handled per Agent Over Time"
                )
                fig.update_layout(height=350)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Utilization trend
                agent_util_trend = filtered_agents.groupby(['month', 'agent_id']).agg({
                    'utilization_pct': 'mean'
                }).reset_index()

                fig = px.line(
                    agent_util_trend,
                    x='month',
                    y='utilization_pct',
                    color='agent_id',
                    markers=True,
                    labels={'month': 'Month', 'utilization_pct': 'Utilization %', 'agent_id': 'Agent'},
                    title="Agent Utilization % Over Time"
                )
                fig.add_hline(y=100, line_dash="dash", line_color="red",
                             annotation_text="100%", annotation_position="right")
                fig.update_layout(height=350)
                st.plotly_chart(fig, use_container_width=True)

            # Agent comparison by hub and function
            if selected_hub == 'All' and selected_function == 'All':
                st.markdown("---")
                st.markdown("**🏢 Agent Metrics by Hub & Function:**")

                agent_hub_function = filtered_agents.groupby(['hub', 'function']).agg({
                    'tickets_handled': 'sum',
                    'utilization_pct': 'mean',
                    'agent_id': 'nunique'
                }).round(2).reset_index()

                agent_hub_function.columns = ['Hub', 'Function', 'Total Tickets', 'Avg Utilization %', 'Agent Count']

                st.dataframe(agent_hub_function, use_container_width=True)

                col1, col2 = st.columns(2)

                with col1:
                    fig = px.bar(
                        agent_hub_function,
                        x='Function',
                        y='Total Tickets',
                        color='Hub',
                        barmode='group',
                        title="Total Tickets by Function & Hub",
                        color_discrete_map={'A': '#1f77b4', 'B': '#ff7f0e'}
                    )
                    fig.update_layout(height=300)
                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    fig = px.bar(
                        agent_hub_function,
                        x='Function',
                        y='Avg Utilization %',
                        color='Hub',
                        barmode='group',
                        title="Average Utilization % by Function & Hub",
                        color_discrete_map={'A': '#1f77b4', 'B': '#ff7f0e'}
                    )
                    fig.update_layout(height=300)
                    st.plotly_chart(fig, use_container_width=True)

            # Agent efficiency metrics
            st.markdown("---")
            st.markdown("**⚙️ Agent Efficiency Metrics:**")

            col1, col2, col3 = st.columns(3)

            with col1:
                total_agents = filtered_agents['agent_id'].nunique()
                st.metric("Total Active Agents", f"{total_agents}")

                avg_tickets_per_agent = filtered_agents['tickets_handled'].sum() / len(filtered_agents)
                st.metric("Avg Tickets per Agent-Month", f"{avg_tickets_per_agent:.1f}")

            with col2:
                avg_utilization = filtered_agents['utilization_pct'].mean()
                st.metric("Average Utilization", f"{avg_utilization:.1f}%")

                over_utilized = (filtered_agents['utilization_pct'] > 100).sum()
                st.metric("Over-Utilized Instances", f"{over_utilized}")

            with col3:
                avg_hours_per_ticket = filtered_agents['avg_hours_per_ticket'].mean()
                st.metric("Avg Hours per Ticket", f"{avg_hours_per_ticket:.2f}h")

                total_ticket_hours = filtered_agents['ticket_work_hours'].sum()
                st.metric("Total Ticket Work Hours", f"{total_ticket_hours:.0f}h")

        else:
            st.info("No agent performance data available.")

        st.markdown("---")

        # Summary statistics
        st.subheader("📊 Summary Statistics")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**Overall Performance**")
            st.metric("Total Tickets Processed", f"{filtered_kpis['total_tickets'].sum():,.0f}")
            st.metric("Average SLA Compliance", f"{filtered_kpis['sla_compliance_pct'].mean():.1f}%")
            st.metric("Total Backlog", f"{filtered_kpis['backlog_count'].sum():,.0f}")

        with col2:
            st.markdown("**Resolution Metrics**")
            st.metric("Avg Resolution Time", f"{filtered_kpis['avg_resolution_time_hours'].mean():.1f} hrs")
            st.metric("Avg Reopen Rate", f"{filtered_kpis['reopen_rate_pct'].mean():.1f}%")
            st.metric("Total Reopened", f"{filtered_kpis['reopen_count'].sum():,.0f}")

        with col3:
            st.markdown("**Customer Satisfaction**")
            st.metric("Average CSAT Score", f"{filtered_kpis['csat_avg_score'].mean():.2f}/5")
            st.metric("Total CSAT Responses", f"{filtered_kpis['csat_responses'].sum():,.0f}")
            st.metric("High CSAT Rate", f"{filtered_kpis['csat_high_pct'].mean():.1f}%")

    # ========================================================================
    # FOOTER
    # ========================================================================

    st.markdown("---")
    st.markdown(f"""
        <div style='text-align: center; color: #666; padding: 1rem;'>
            <p><strong>Support Operations Dashboard</strong> | OrionEdge Corp</p>
            <p>Data Range: {filtered_tickets['created_datetime'].min().date()} to {filtered_tickets['created_datetime'].max().date()}</p>
            <p>Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    """, unsafe_allow_html=True)

# ============================================================================
# RUN APP
# ============================================================================

if __name__ == "__main__":
    main()
