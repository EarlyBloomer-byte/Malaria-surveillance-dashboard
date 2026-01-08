# app.py
import streamlit as st
from data_manager import generate_dummy_data, get_kpi_metrics, fetch_malaria_news
from visuals import plot_trend_chart, plot_map, plot_donut_chart, plot_animated_map, plot_animated_bar_race
from report_generator import generate_malaria_pdf
from AI_assistant import setup_ai, get_ai_response

# --- Page Configuration ---
st.set_page_config(page_title="Malaria Surveillance & Monitoring Dashboard", page_icon="🦟", layout="wide")

# --- Custom Styling ---
st.markdown("""
<style>
    .metric-card { background-color: #f8f9fa; border-radius: 8px; padding: 15px; border: 1px solid #eee; text-align: center; }
    .news-card { background-color: white; border-left: 5px solid #007bff; padding: 15px; margin-bottom: 15px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    [data-testid="stMetricValue"] { font-size: 24px; }
</style>
""", unsafe_allow_html=True)

# --- 1. Sidebar (Global Controls) ---
with st.sidebar:
    st.title("🎛️ Menu")
    raw_df = generate_dummy_data()
    
    selected_year = st.selectbox("Reporting Year", sorted(raw_df['Date'].dt.year.unique(), reverse=True))
    selected_region = st.radio("Focus Region", ["All"] + list(raw_df['Region'].unique()))
    
    st.divider()
    st.info("This dashboard provides real-time surveillance data for malaria control programs.")

# --- Data Filtering Logic ---
df_filtered = raw_df[raw_df['Date'].dt.year == selected_year]
if selected_region != "All":
    df_filtered = df_filtered[df_filtered['Region'] == selected_region]

# --- 2. Main Header ---
st.title("🦟 Malaria Surveillance & Intelligence Portal")
st.caption(f"Showing data for: **{selected_region} Region** | Year: **{selected_year}**")

# --- 3. Dashboard Tabs ---
tab_overview, tab_analytics, tab_animations, tab_news, tab_ai = st.tabs([
    "📍 Surveillance Overview", 
    "📊 Trends & Analytics",
    "📽️ Time-Lapse", 
    "📰 Intelligence & News",
    "🤖 AI Assistant"
])

# TAB 1: OVERVIEW
with tab_overview:
    # KPI Row
    cases, recoveries, prevalence, risk = get_kpi_metrics(df_filtered)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Cases", f"{cases:,}", "+5%") # Example delta
    c2.metric("Recoveries", f"{recoveries:,}", "2%", delta_color="normal")
    c3.metric("Avg Prevalence", f"{prevalence:.1f}%")
    c4.metric("Risk Level", risk)

    st.write("------")
    
    # Map and Distribution
    col_map, col_pie = st.columns([2, 1])
    with col_map:
        st.subheader("Geographic Incidence")
        st.plotly_chart(plot_map(df_filtered), use_container_width=True)
    with col_pie:
        st.subheader("Outcome Split")
        st.plotly_chart(plot_donut_chart(df_filtered), use_container_width=True)

# TAB 2: ANALYTICS
with tab_analytics:
    st.subheader("Incidence Trends")
    st.plotly_chart(plot_trend_chart(df_filtered), use_container_width=True)
    
    st.subheader("Regional Comparative Data")
    # Quick Pivot Table
    pivot = df_filtered.pivot_table(index='Region', values=['Cases', 'Deaths'], aggfunc='sum')
    st.dataframe(pivot, use_container_width=True)

# TAB 3: NEWS & UPDATES
with tab_news:
    st.subheader("Latest Field Reports & Global Health News")
    news_data = fetch_malaria_news(selected_region)
    
    for item in news_data:
        st.markdown(f"""
        <div class="news-card">
            <small style="color:gray">{item['date']} | Source: {item['source']}</small>
            <div style="font-weight:bold; font-size:18px; color:#007bff; margin: 5px 0;">{item['title']}</div>
            <div style="font-size:14px; margin-bottom:10px;">{item['summary']}</div>
            <a href="{item['link']}" style="text-decoration:none; color:#e74c3c; font-weight:bold;">Read Article →</a>
        </div>
        """, unsafe_allow_html=True)

if not news_data:
    st.info(f"No specific recent updates found for the {selected_region} region.")


# TAB 4: ANIMATIONS
with tab_animations:
    st.subheader("Temporal Disease Dynamics")
    st.markdown("Press **Play** to visualize how malaria cases spread and shift over the year.")
    
    # Map Animation
    st.plotly_chart(plot_animated_map(df_filtered), use_container_width=True)
    
    st.divider()
    
    # Bar Animation
    st.subheader("Regional Ranking Race")
    st.markdown("Observe which regions experience spikes in different months.")
    st.plotly_chart(plot_animated_bar_race(df_filtered), use_container_width=True)


st.sidebar.markdown("---")
st.sidebar.subheader("📤 Export Center")

if st.sidebar.button("🛠️ Generate Final Report"):
    with st.spinner("Compiling data and charts..."):
        # 1. Prepare KPIs
        cases, recoveries, prevalence, risk = get_kpi_metrics(df_filtered)
        kpi_data = [
            ("Total Cases", f"{cases:,}"),
            ("Avg Prevalence", f"{prevalence:.1f}%"),
            ("Regional Risk Status", risk)
        ]
        
        # 2. Prepare static charts ( this is to nsure these functions return a fig)
        chart_dict = {
            "Case Trends": plot_trend_chart(df_filtered),
            "Geographic Map": plot_map(df_filtered)
        }
        
        # 3. Call generator
        try:
            final_pdf = generate_malaria_pdf(df_filtered, kpi_data, chart_dict)
            
            # 4. To Display download button after compiling.
            st.sidebar.success("✅ Report Ready!")
            st.sidebar.download_button(
                label="📥 Download PDF",
                data=final_pdf,
                file_name=f"Malaria_Surveillance_{selected_year}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.sidebar.error(f"Error generating report: {e}")

if "messages" not in st.session_state:
    st.session_state.messages = []

# TAB 5: AI Assitant

with tab_ai:
    st.header("🤖 Malaria Expert AI")
    st.info("Ask me about the current data or WHO malaria protocols.")

    # Display chat history from session state
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("Ex: What should we do about the case spike in the North?"):
        # Display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate AI Context from my dashboard variables
        cases, _, _, risk = get_kpi_metrics(df_filtered) # Get current metrics
        context = f"Region: {selected_region}, Total Cases: {cases}, Risk Level: {risk}"

        # Get AI Response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                model = setup_ai("YOUR_GEMINI_API_KEY_HERE") 
                response = get_ai_response(model, prompt, context)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})