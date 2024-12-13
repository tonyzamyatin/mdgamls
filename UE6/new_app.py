import streamlit as st
import pandas as pd
from data import get_cleaned_and_sorted_data
from ts_analysis import auto_fit_arima
from interactive_plot import plot_trends_interactive, plot_forecast_with_ci_interactive

# Load the data
df = get_cleaned_and_sorted_data()

# TITLE AND DESCRIPTION
st.title('Visual Analysis of COVID-19, Pneumonia, and Influenza Deaths in the U.S.')
st.markdown(
    """ 
    The data is sourced from the CDC's official
    [Provisional COVID-19 Death Counts by Week Ending Date and State](https://data.cdc.gov/NCHS/Provisional-COVID-19-Death-Counts-by-Week-Ending-D/r8kw-7aab/about_data) dataset.
    """
)

# INTERACTIVE PLOT FOR ALL METRICS
st.sidebar.header("Settings")
state = st.sidebar.selectbox("Select a State", options=df['State'].unique())

# Filter data for the selected state
df_state = df[df['State'] == state]

st.header(f"Weekly Death Trends in {state}")
metrics = [
    "COVID-19",
    "Pneumonia",
    "Influenza",
    "Pneumonia & COVID-19",
    "Undiagnosed",
]

# Plot all metrics for the selected state
fig_all_metrics = plot_trends_interactive(df_state, metrics, state)
st.plotly_chart(fig_all_metrics)

# FORECAST SECTION
CI_ALPHA = 0.05

st.header("Forecast for a Specific Metric")
selected_metric = st.selectbox("Select a Metric", options=metrics)
forecast_steps = st.slider("Select Number of Weeks for Forecast", min_value=1, max_value=52, value=10)


# Compute the time series for the selected metric only once and store it in session state
timeseries_name = f"timeseries_{selected_metric}_{state}"
if timeseries_name not in st.session_state:
    timeseries = df_state.set_index('End Date')[selected_metric]
    st.session_state[timeseries_name] = timeseries

# Retrieve the time series from session state
timeseries = st.session_state[timeseries_name]

# Compute Auto ARIMA model only once and store it in session state
model_name = f"arima_model_{selected_metric}"
if model_name not in st.session_state:
    with st.spinner("Fitting ARIMA model..."):
        st.session_state[model_name] = auto_fit_arima(timeseries, seasonal=True, alpha=CI_ALPHA)

# Retrieve the ARIMA model from session state
arima_model = st.session_state[model_name]

# Compute forecast and confidence intervals only once and store them in session state
forecast_name = f"forecast_{selected_metric}_{state}_{forecast_steps}"
if forecast_name not in st.session_state:
    with st.spinner("Computing forecast..."):
        forecast_values, forecast_conf_int = arima_model.predict(n_periods=forecast_steps, return_conf_int=True)
        forecast_index = pd.date_range(start=timeseries.index[-1] + pd.Timedelta(days=7), periods=forecast_steps, freq="W-SAT")
        forecast_series = pd.Series(forecast_values, index=forecast_index)
        conf_int_df = pd.DataFrame(
            forecast_conf_int, index=forecast_index, columns=["Lower CI", "Upper CI"]
        )
        st.session_state[forecast_name] = (forecast_series, conf_int_df)

# Retrieve the forecast and confidence intervals from session state
forecast_series, conf_int_df = st.session_state[forecast_name]

# Plot the forecast with confidence intervals
forecast_plot = plot_forecast_with_ci_interactive(timeseries, forecast_series, conf_int_df, CI_ALPHA, selected_metric, state, ylim=(0, None))
st.plotly_chart(forecast_plot)
