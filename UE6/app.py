import streamlit as st
import pandas as pd

from FilteringTrends import filter_data, plot_trend

st.title('Visual Analysis of COVID-19, Pneumia and Influenza Deaths')
st.markdown('Includes analysis of time-series data of **COVID-19, Pneumia and Influenza** to spot **peaks, declines, anomalies and correlations**.')


st.header('Overview Data')
st.markdown('Checkout the first 5 rows of the table here, to get an idea what data it contains. should we describe in more detail here?')
df = pd.read_csv('Provisional_COVID-19_Death_Counts_by_Week_Ending_Date_and_State_20241211.csv')
st.write(df.head())

st.header("Weekly Death Trends Over Time")

year = st.selectbox("Select a Year to Filter:", options=['2024', '2023', '2022', '2021', '2020'])

options_state = df['State'].unique()
state = st.selectbox("Select a State to Filter:", options=options_state)

df_trend = filter_data(df, year, state)
plt = plot_trend(df_trend, state, year)

st.pyplot(plt)