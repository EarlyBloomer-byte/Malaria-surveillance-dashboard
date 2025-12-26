# visuals.py
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go

def plot_trend_chart(df):
    """Line chart showing cases over time by region."""
    fig = px.line(
        df, x='Date', y='Cases', color='Region',
        title='Malaria Incidence Trends',
        markers=True,
        template="presentation"
    )
    fig.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))
    return fig

def plot_map(df):
    """Bubble map showing outbreaks."""
    # Group by location for map stability
    map_data = df.groupby(['Region', 'Latitude', 'Longitude'])['Cases'].sum().reset_index()
    
    fig = px.scatter_mapbox(
        map_data, lat="Latitude", lon="Longitude",
        size="Cases", color="Cases",
        hover_name="Region",
        zoom=5, height=400,
        color_continuous_scale="Reds",
        mapbox_style="carto-positron" # Clean map style
    )
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    return fig

def plot_donut_chart(df):
    """Donut chart for outcome distribution."""
    total_deaths = df['Deaths'].sum()
    total_recoveries = df['Recoveries'].sum()
    
    labels = ['Recoveries', 'Deaths']
    values = [total_recoveries, total_deaths]
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6)]) # .6 , 300
    fig.update_layout(
        title="Outcome Distribution", 
        height=300,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig