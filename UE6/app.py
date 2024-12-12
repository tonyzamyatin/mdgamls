import streamlit as st
import pandas as pd

from FilteringTrends import filter_data, plot_trend
from ComparingStates import filter_sum, plot_comparison

st.title('Visual Analysis of COVID-19, Pneumia and Influenza Deaths')
st.markdown('Includes analysis of time-series data of **COVID-19, Pneumia and Influenza** to spot **peaks, declines, anomalies and correlations**.')


st.header('Overview Data')
st.markdown('Checkout the first 5 rows of the table here, to get an idea what data it contains. should we describe in more detail here?')
df = pd.read_csv('Provisional_COVID-19_Death_Counts_by_Week_Ending_Date_and_State_20241211.csv')
st.write(df.head())

st.header("Weekly Death Trends Over Time")
year_trend = st.selectbox("Select a Year to Filter:", options=['2024', '2023', '2022', '2021', '2020'])

options_state = df['State'].unique()
state_trend = st.selectbox("Select a State to Filter:", options=options_state)

df_trend = filter_data(df, year_trend, state_trend)
plt_trend = plot_trend(df_trend, state_trend, year_trend)
st.pyplot(plt_trend)

st.header("Compare statistics")
st.markdown("Here I want to enable users to compare death situations of max 5 states at the same time")
states_compare = st.multiselect("Select states to compare", options=options_state, placeholder="Choose up to 5 states", max_selections=5)
year_compare = st.selectbox("Select year at which to compare", options=['2024', '2023', '2022', '2021', '2020'])
month_compare = st.selectbox("Select month at which to compare", options=[ 'No month selected', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

state_sums = filter_sum(df, year_compare, states_compare, month_compare)
if states_compare:
    plt_compare = plot_comparison(state_sums, year_compare, month_compare)
    st.pyplot(plt_compare)