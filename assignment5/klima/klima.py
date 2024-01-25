# klima.py

import pandas as pd
import altair as alt
import datetime
import calendar


def fetch_and_process_data():
    # Fetch and process data from anomalies and monthly mean temperature data
    # Calculate the mean temperature for each month for different years
    # Return a Pandas DataFrame with the processed data
    try:
        df_anomalies = pd.read_csv("data.csv")

        # Monthly mean temperature data
        monthly_data = {
            "Month": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
            "Mean_Temperature": [12.0, 12.1, 12.7, 13.7, 14.8, 15.5, 15.8, 15.6, 15.0, 14.0, 12.9, 12.2],
        }
         # Create a mapping of month names to month numbers
        month_name_to_number = {name: num for num, name in enumerate(calendar.month_name[1:], start=1)}

        df_monthly = pd.DataFrame(monthly_data)

        df = pd.merge(df_anomalies, df_monthly, on='Month')

        print(df.head()) 

        df['Year'] = df['YearMonth'] // 100

        return df
    
    except FileNotFoundError:
        print("Error: File not found.")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()

def create_interactive_chart():
    global chart

    current_year = datetime.date.today().year
    df = fetch_and_process_data()

    # Print DataFrame for debugging
    print(df.head())

    if len(df) == 0:
        print("Error: Empty DataFrame.")
        return None  # or handle the error appropriately

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

    # Print the chart for debugging
    print(chart)

    return chart


def create_tooltip_data(df, year):
    # Extract tooltip data for the specified year
    # Return a dictionary containing the tooltip information
    tooltip_data = df[df['Year'] == year][['Month', 'Mean_Temperature']]
    tooltip_dict = tooltip_data.to_dict('records')
    return tooltip_dict
