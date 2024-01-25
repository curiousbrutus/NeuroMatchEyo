#!/usr/bin/env python3
"""
Fetch data from https://www.hvakosterstrommen.no/strompris-api
and visualize it.

Assignment 5
"""


import warnings
import altair as alt
import pandas as pd
import requests
import datetime
import requests_cache
from typing import List, Optional
# install an HTTP request cache
# to avoid unnecessary repeat requests for the same data
# this will create the file http_cache.sqlite
requests_cache.install_cache()

# suppress a warning with altair 4 and latest pandas
warnings.filterwarnings("ignore", ".*convert_dtype.*", FutureWarning)


# task 5.1:


def fetch_day_prices(date: datetime.date = None, location: str = "NO1") -> pd.DataFrame:
    """Fetch one day of data for one location from hvakosterstrommen.no API

    Make sure to document arguments and return value...
    ...
    """
    if date is None:
        date = datetime.date.today()

    #raise NotImplementedError("Remove me when you implement this task")

    url = f"https://www.hvakosterstrommen.no/api/v1/prices/{date.year}/{date.month:02d}-{date.day:02d}_{location}.json"
    response = requests.get(url)

    if response.status_code == 200:
# Extract the relevant data from the response 
        #print(response.json())
        data = response.json()
# create a dataframe
        df = pd.DataFrame(data)
        df.astype({'NOK_per_kWh': 'float64'})
        df['time_start'] = pd.to_datetime(df['time_start'], utc=True).dt.tz_convert('Europe/Oslo')
        return df 

    else:
# if it is not succesful
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return pd.DataFrame


# LOCATION_CODES maps codes ("NO1") to names ("Oslo")
LOCATION_CODES = {
    "NO1": "Oslo",
    "NO2": "Kristiansand",
    "NO3": "Trondheim",
    "NO4": "Tromsø",
    "NO5": "Bergen",
}

# task 1:


def fetch_prices(
    end_date: datetime.date = None,
    days: int = 7,
    locations: Optional[List[str]] = None,
    activity: str = None,
) -> pd.DataFrame:
    """Fetch prices for multiple days and locations into a single DataFrame

    Make sure to document arguments and return value...
    ...
    """
    #raise NotImplementedError("Remove me when you implement this task")
    
    if end_date is None:
        end_date = datetime.date.today()
    if locations is None:
        locations = tuple(LOCATION_CODES.keys())

    result_df = pd.DataFrame()

    # Initialize an empty Dataframe to store the results 
    for day in range(days):
        date_to_fetch = end_date - datetime.timedelta(days=day)

        for location_code in locations:
                day_prices = fetch_day_prices(date_to_fetch, location_code)
                print(day_prices.columns)
 
                #Add location information to the dataframe
                day_prices['location_code'] = location_code
                day_prices['location'] = LOCATION_CODES[location_code]

                # Add 1h, 24h, and 7d changes
                day_prices['1h_change'] = day_prices['NOK_per_kWh'].diff()
                day_prices['24h_change'] = day_prices['NOK_per_kWh'].diff(24)
                day_prices['7d_change'] = day_prices['NOK_per_kWh'].diff(7 * 24)

                result_df = pd.concat([result_df, day_prices], ignore_index=True)

    print(result_df)
    return result_df

'''


    url = f"https://www.hvakosterstrommen.no/api/v1/prices/{end_date.year}/{end_date.month:02d}-{end_date.day:02d}_{locations}.json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        result_df = pd.DataFrame(data)

        if activity is not None:
            energy_usage = ACTIVITIES.get(activity, 1.0)
            result_df['NOK_per_kWh'] *= energy_usage
    '''    


            
#       Concanate the results
            




# task 5.1:


def plot_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot energy prices over time

    x-axis should be time_start
    y-axis should be price in NOK
    each location should get its own line

    Make sure to document arguments and return value...
    """
    #raise NotImplementedError("Remove me when you implement this task")
    chart = alt.Chart(df).mark_line().encode(
        x='time_start:T',
        y='NOK_per_kWh:Q',
        color='location:N',
        tooltip=['time_start:T', 'NOK_per_kWh:Q', 'location:N']
    ).properties(
        title='Energy Prices by Date and Location',
        width=800,
        height=400,
    )

    return chart


# Task 5.4


def plot_daily_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot the daily average price

    x-axis should be time_start (day resolution)
    y-axis should be price in NOK

    You may use any mark.

    Make sure to document arguments and return value...
    """
    #raise NotImplementedError("Remove me when you implement this task (in4110 only)")
    daily_avg_chart = alt.Chart(df).mark_line().encode(
        x=alt.X('time_start:T', timeUnit='day'),
        y=alt.Y('mean(NOK_per_kWh):Q', title='Daily Average Price (NOK)'),
        color='location:N',
        tooltip=['time_start:T', 'mean(NOK_per_kWh):Q', 'location:N']
    ).properties(
        title='Daily Average Energy Prices by Location',
        width=800,
        height=400,
    )

    return daily_avg_chart


# Task 5.6

ACTIVITIES = {
    # activity name: energy cost in kW
    "shower": 30,
    "baking": 2.5,
    "heat": 1,
}


def plot_activity_prices(df: pd.DataFrame, activity: str = "shower", minutes: float = 10
) -> alt.Chart:
    """
    Plot price for one activity by name,
    given a data frame of prices, and its duration in minutes.

    Make sure to document arguments and return value...
    """
    #raise NotImplementedError("Remove me when you implement this optional task")
    total_cost = df['NOK_per_kWh'].sum() * minutes 

    chart = alt.Chart(pd.DataFrame({'Activity': [activity], 'Total Cost': [total_cost]})).mark_bar().encode(
        x='Activity:N',
        y='Total Cost:Q',
        tooltip=['Activity:N', 'Total Cost:Q']
    ).properties(
        title=f'Total Cost for {activity} ({minutes} minutes)',
        width=800,
        height=400,
    )

    return chart  


def main():
    """Allow running this module as a script for testing."""
    df = fetch_prices()
    print(df)
    chart = plot_prices(df)
    daily_avg_chart = plot_daily_prices(df)
    activity_chart = plot_activity_prices(df, activity='shower', minutes=10)
    
    # showing the chart without requiring jupyter notebook or vs code for example
    # requires altair viewer: `pip install altair_viewer`
    
    combined_chart = alt.hconcat(chart, daily_avg_chart)  # Combine charts horizontally
    combined_chart.show()
    #chart.show()


if __name__ == "__main__":
    main()
