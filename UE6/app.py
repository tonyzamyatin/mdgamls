from calendar import month

import streamlit as st
import pandas as pd

from FilteringTrends import filter_data, plot_trend
from data import clean_data, get_raw_data

df = get_raw_data()
print(f"{len(df)} rows")
clean_data(df)
print(f"{len(df)} rows after cleaning")

# TITLE
st.title('Visual Analysis of COVID-19, Pneumia and Influenza Deaths')
st.markdown('Includes analysis of time-series data of **COVID-19, Pneumia and Influenza** to spot **peaks, declines, anomalies and correlations**.')

# OVERVIEW DATA
st.header('Overview Data')
st.markdown('Checkout the first 5 rows of the table here, to get an idea what data it contains. should we describe in more detail here?')
st.write(df.head())

# WEEKLY DEATH TRENDS OVER TIME
st.header("Weekly Death Trends Over Time")
year = st.selectbox("Select a Year to Filter:", options=['2024', '2023', '2022', '2021', '2020'])
options_state = df['State'].unique()
state = st.selectbox("Select a State to Filter:", options=options_state)
df_trend = filter_data(df, year, state)
plt_weekly_deaths_over_year = plot_trend(df_trend, state, year)
st.pyplot(plt_weekly_deaths_over_year)

