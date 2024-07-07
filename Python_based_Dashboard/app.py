import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data # Cache data to avoid loading it multiple times
def load_data():
    df = pd.read_csv('/Users/deveshsharma/Downloads/Python_based_Dashboard/data/Agmarket Prices 2023.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# Streamlit app
st.title('Data Visualization Dashboard using Streamlit and Plotly')

# Sidebar for filters
st.sidebar.header('Filters')
selected_state = st.sidebar.selectbox('Select State', df['census_state_name'].unique())
selected_district = st.sidebar.selectbox('Select District', df[df['census_state_name'] == selected_state]['census_district_name'].unique()) #Selecting unique district values based on states
selected_commodity = st.sidebar.selectbox('Select Commodity', df['commodity_name'].unique())

# Filter data
filtered_df = df[(df['census_state_name'] == selected_state) & 
                 (df['census_district_name'] == selected_district) & 
                 (df['commodity_name'] == selected_commodity)]

# Create heatmap
def create_heatmap(df):
    pivot = df.pivot_table(values='modal_price', index='census_district_name', 
                             columns=df['date'].dt.strftime('%B'), 
                             aggfunc='mean')
    fig = px.imshow(pivot, labels=dict(color="Average Price"),
                    title=f"Monthly Average Modal Price for {selected_commodity} in {selected_state}")
    return fig

# Create line chart
def create_line_chart(df):
    monthly_avg = df.groupby(df['date'].dt.strftime('%B'))['modal_price'].mean().reset_index()
    fig = px.line(monthly_avg, x='date', y='modal_price', 
                  title=f"Monthly Average Modal Price Trend for {selected_commodity} in {selected_state}")
    return fig

# Display visualizations
st.plotly_chart(create_heatmap(filtered_df))
st.plotly_chart(create_line_chart(filtered_df))