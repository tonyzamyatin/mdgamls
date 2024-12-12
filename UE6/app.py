import streamlit as st
import pandas as pd

from FilteringTrends import filter_data, plot_trend
from ComparingStates import filter_sum, plot_comparison

st.set_page_config(layout="wide")
st.title('Visual Analysis of COVID-19, Pneumia and Influenza Deaths')
st.markdown('Includes analysis of time-series data of **COVID-19, Pneumia and Influenza** to spot **peaks, declines, anomalies and correlations**.')


st.header('Overview Data')
st.markdown('Checkout the first 5 rows of the table here, to get an idea what data it contains. should we describe in more detail here?')
df = pd.read_csv('Provisional_COVID-19_Death_Counts_by_Week_Ending_Date_and_State_20241211.csv')
st.write(df.head())
col1_layout, col2_layout = st.columns(2)

with col1_layout:
    st.header("Weekly Death Trends Over Time")
    st.markdown('Follow the course of the number of deaths from pathogens in a specific state for a year.')
    col1_trend, col2_trend = st.columns(2)
    with col1_trend:
        year_trend = st.selectbox("Select a Year to Filter:", options=['2024', '2023', '2022', '2021', '2020'])
    options_state = df['State'].unique()
    with col2_trend:
        state_trend = st.selectbox("Select a State to Filter:", options=options_state)
    df_trend = filter_data(df, year_trend, state_trend)
    plt_trend = plot_trend(df_trend, state_trend, year_trend)
    st.pyplot(plt_trend)

with col2_layout:
    st.header("Compare statistics")
    st.markdown("Compare number of deaths from pathogens of max 5 states at the same point in time.")
    col1_compare, col2_compare, col3_compare = st.columns([3,1,1])
    with col1_compare:
        states_compare = st.multiselect("Select States to Compare", options=options_state, placeholder="Choose up to 5 states", max_selections=5)
    with col2_compare:
        year_compare = st.selectbox("Select Year", options=['2024', '2023', '2022', '2021', '2020'])
    with col3_compare:
        month_compare = st.selectbox("Select Month", options=[ 'No month selected', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

    state_sums = filter_sum(df, year_compare, states_compare, month_compare)
    if states_compare:
        plt_compare = plot_comparison(state_sums, year_compare, month_compare)
        st.pyplot(plt_compare)