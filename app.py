# app.py
import streamlit as st
import pandas as pd
from data_manager import generate_dummy_data, get_kpi_metrics
from visuals import plot_trend_chart, plot_map, plot_donut_chart

# --- Page Configuration ---
st.set_page_config(
    page_title="Malaria Surveillance and Monitoring Dashboard",
    page_icon="🦟",
    layout="wide"
)

# --- CSS Styling for "Cards" ---
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    .metric-title { font-size: 16px; color: #555; margin-bottom: 5px; }
    .metric-value { font-size: 28px; font-weight: bold; color: #000; }
    .risk-high { color: #e74c3c; }
    .risk-mod { color: #f39c12; }
</style>
""", unsafe_allow_html=True)

# --- Sidebar: Filters ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2855/2855263.png", width=50) # Placeholder Icon
    st.header("Filters")
    
    # Load Data
    raw_df = generate_dummy_data()
    
    # Year Filter
    years = raw_df['Date'].dt.year.unique()
    selected_year = st.selectbox("Select Year", years)
    
    # Region Filter
    all_regions = ["All"] + list(raw_df['Region'].unique())
    selected_region = st.selectbox("Select Region", all_regions)

# --- Data Filtering Logic ---
df_filtered = raw_df[raw_df['Date'].dt.year == selected_year]
if selected_region != "All":
    df_filtered = df_filtered[df_filtered['Region'] == selected_region]

# --- Main Dashboard ---
st.title(f"🦟 Malaria Surveillance Dashboard ({selected_year})")
st.markdown("Real-time monitoring of incidence, prevalence, and recovery rates.")
st.divider()

# 1. Summary Cards (KPIs)
cases, recoveries, prevalence, risk = get_kpi_metrics(df_filtered)

c1, c2, c3, c4 = st.columns(4)

def metric_card(col, title, value, color="black"):
    col.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value" style="color: {color}">{value}</div>
    </div>
    """, unsafe_allow_html=True)

metric_card(c1, "Total Cases", f"{cases:,}")
metric_card(c2, "Recoveries", f"{recoveries:,}", "#27ae60")
metric_card(c3, "Avg Prevalence", f"{prevalence:.1f}%")
metric_card(c4, "Risk Level", risk, "#e74c3c" if risk == "High" else "#f39c12")

st.write("") # Spacer

# 2. Main Charts Row
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("Regional Outbreak Map")
    st.plotly_chart(plot_map(df_filtered), use_container_width=True)

with col_right:
    st.subheader("Outcome Analysis")
    st.plotly_chart(plot_donut_chart(df_filtered), use_container_width=True)

# 3. Trends Row
st.subheader("Incidence Trends Over Time")
st.plotly_chart(plot_trend_chart(df_filtered), use_container_width=True)

# 4. Raw Data Expander
with st.expander("View Raw Data"):
    st.dataframe(df_filtered)