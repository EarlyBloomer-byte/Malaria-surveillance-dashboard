# data_manager.py
import pandas as pd
import numpy as np
import datetime

def generate_dummy_data():
    """Generates synthetic malaria data for demonstration."""
    regions = ['North', 'South', 'East', 'West', 'Central']
    dates = pd.date_range(start='2020-01-01', end='2025-12-31', freq='M')
    
    data = []
    
    for region in regions:
        # Simulate lat/lon for the region (approximate centers)
        lat, lon = {
            'North': (10.0, 8.0), 'South': (5.0, 7.0),
            'East': (8.0, 11.0), 'West': (9.0, 4.0),
            'Central': (9.0, 7.0)
        }[region]
        
        for date in dates:
            # Randomize incidence with some seasonality
            base_cases = np.random.randint(500, 1500)
            if date.month in [6, 7, 8]: # Rainy season peak
                base_cases += np.random.randint(500, 1000)
                
            data.append({
                'Date': date,
                'Region': region,
                'Latitude': lat + np.random.uniform(-0.5, 0.5),
                'Longitude': lon + np.random.uniform(-0.5, 0.5),
                'Cases': base_cases,
                'Recoveries': int(base_cases * 0.85),
                'Deaths': int(base_cases * 0.05),
                'Prevalence_Rate': np.random.uniform(10, 25) # %
            })
            
    return pd.DataFrame(data)

def get_kpi_metrics(df):
    """Calculates summary metrics for cards."""
    total_cases = df['Cases'].sum()
    total_recoveries = df['Recoveries'].sum()
    avg_prevalence = df['Prevalence_Rate'].mean()
    risk_level = "High" if avg_prevalence > 20 else "Moderate"
    
    return total_cases, total_recoveries, avg_prevalence, risk_level

def fetch_malaria_news(region="All"):
    """
    Fetches latest malaria updates .
    I plan to connect with an API after connecting with this
    """
    # Real-world data based on Dec 2025 reports
    news_items = [
        {
            "date": "Dec 04, 2025",
            "title": "WHO Releases World Malaria Report 2025",
            "summary": "The 2025 report highlights a slight increase in global cases to 282 million, emphasizing the growing threat of drug resistance.",
            "source": "World Health Organization",
            "link": "https://www.who.int/news-room/fact-sheets/detail/malaria"
        },
        {
            "date": "Nov 15, 2025",
            "title": "Breakthrough in Non-Artemisinin Treatments",
            "summary": "Phase 3 trials for GanLum show positive results, offering a potential new tool against artemisinin-resistant parasites.",
            "source": "Medicines for Malaria Venture",
            "link": "https://www.mmv.org/newsroom"
        },
        {
            "date": "Oct 24, 2025",
            "title": "New Vaccine Rollout in Central Africa",
            "summary": "Targeted vaccination campaigns reach 1 million children in high-transmission zones this quarter.",
            "source": "Global Fund Updates",
            "link": "https://www.theglobalfund.org/"
        }
    ]
    
    # Simple filtering logic for the demonstration
    if region != "All":
        # In a real API call, I would pass the region as a search parameter
        return [item for item in news_items if region.lower() in item['summary'].lower()]
        
    return news_items