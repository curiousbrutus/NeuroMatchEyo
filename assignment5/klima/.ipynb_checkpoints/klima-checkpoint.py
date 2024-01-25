# klima.py

import pandas as pd
import altair as alt
import re

import datetime

def fetch_and_process_data():
    # Fetch and process data from the provided links
    # Combine anomalies and monthly mean temperature data
    # Calculate the mean temperature for each month for different years
    # Return a Pandas DataFrame with the processed data
    df = pd.read_csv("data_antartica.csv")
    
    return df

def create_interactive_chart():
    # Create an interactive line plot using Altair or another library
    # Highlight the current year's data boldly
    # Implement tooltips for each data point
    current_year = datetime.date.today().year

    chart = alt.Chart(df).mark_line().encode(
        x='Month:T',
        y=alt.Y('Mean_Temperature:Q', title='Mean Temperature (°C)'),
        color=alt.Color('Year:N', scale=alt.Scale(scheme='category20')),
        tooltip=['Month:T', 'Mean_Temperature:Q', 'Year:N']
    ).properties(
        title='Global Average Temperature Over Time',
        width=800,
        height=400,
    ).interactive()

    return chart

def create_tooltip_data(df, year):
    # Extract tooltip data for the specified year
    # Return a dictionary containing the tooltip information
    
    tooltip_data = df[df['Year'] == year][['Month', 'Mean_Temperature']]
    tooltip_dict = tooltip_data.to_dict('records')
    return tooltip_dict