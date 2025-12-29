# app.py
import streamlit as st
from data_manager import generate_dummy_data, get_kpi_metrics, fetch_malaria_news
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
        background-color: #FFFFFF;
        border-radius: 15px;
        padding: 30px;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    .metric-title { font-size: 16px; color: #555; margin-bottom: 5px; }
    .metric-value { font-size: 28px; font-weight: bold; color: #000; }
    .risk-high { color: #e74c3c; }
    .risk-mod { color: #f39c12; }
</style>
""", unsafe_allow_html=True) #f0ff2f6 f0f2f6

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

# --- NEW: CSS for News Cards ---
st.markdown("""
<style>
    .news-card {
        background-color: #ffffff;
        border-left: 5px solid #e74c3c;
        padding: 15px;
        margin-bottom: 10px;
        border-radius: 5px;
        box-shadow: 1px 1px 3px rgba(0,0,0,0.1);
    }
    .news-date { font-size: 12px; color: #888; }
    .news-title { font-weight: bold; font-size: 16px; margin: 5px 0; color: #1f77b4; }
    .news-summary { font-size: 14px; color: #333; }
</style>
""", unsafe_allow_html=True)

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

# ---------------------------------------------------------
# NEW SECTION: Recent News & Updates
# ---------------------------------------------------------
st.divider()
st.subheader("📰 Latest Intelligence & Field Updates")

news_data = fetch_malaria_news(selected_region)

# Display news in a 4-column grid
cols = st.columns(3)
for i, item in enumerate(news_data):
    with cols[i % 3]:
        st.markdown(f"""
        <div class="news-card">
            <div class="news-date">{item['date']} | {item['source']}</div>
            <div class="news-title">{item['title']}</div>
            <div class="news-summary">{item['summary']}</div>
            <a href="{item['link']}" target="_blank" style="font-size: 12px; color: #e74c3c;">Read Full Article →</a>
        </div>
        """, unsafe_allow_html=True)

if not news_data:
    st.info(f"No specific recent updates found for the {selected_region} region.")