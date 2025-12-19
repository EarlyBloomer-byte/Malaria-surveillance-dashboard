# data_manager.py
import pandas as pd
import numpy as np
import datetime

def generate_dummy_data():
    """Generates synthetic malaria data for demonstration."""
    regions = ['North', 'South', 'East', 'West', 'Central']
    dates = pd.date_range(start='2023-01-01', periods=12, freq='M')
    
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