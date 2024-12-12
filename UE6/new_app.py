import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data import get_raw_data, clean_data
from ts_analysis import auto_fit_arima, plot_forecast_with_confidence_intervals_interactive

# Load and clean the data
df = get_raw_data()
columns_rename_map = {
    'COVID-19 Deaths': 'COVID-19',
    'Total Deaths': 'Total',
    'Pneumonia Deaths': 'Pneumonia',
    'Pneumonia and COVID-19 Deaths': 'Pneumonia & COVID-19',
    'Influenza Deaths': 'Influenza',
    'Pneumonia, Influenza, or COVID-19 Deaths': 'Undiagnosed'
}

df.rename(columns=columns_rename_map, inplace=True)
df_cleaned = clean_data(df)

# Sort the data by 'End Date'
df_cleaned.sort_values(by='End Date', inplace=True)

# TITLE AND DESCRIPTION
st.title('Visual Analysis of COVID-19, Pneumonia, and Influenza Deaths')
st.markdown(
    """
    Includes analysis of time-series data of **COVID-19, Pneumonia, and Influenza** 
    to spot **peaks, declines, anomalies, and correlations**.
    """
)

# INTERACTIVE PLOT FOR ALL METRICS
st.sidebar.header("Settings")
state = st.sidebar.selectbox("Select a State", options=df_cleaned['State'].unique())

# Filter data for the selected state
df_state = df_cleaned[df_cleaned['State'] == state]

# Step 2: Interactive Plot for All Metrics
st.header(f"Weekly Death Trends in {state}")
metrics = [
    "COVID-19",
    "Pneumonia",
    "Influenza",
    "Pneumonia & COVID-19",
    "Undiagnosed",
]

# Create a Plotly figure
fig_all_metrics = make_subplots(rows=1, cols=1)

# Add traces for each metric
for metric in metrics:
    fig_all_metrics.add_trace(
        go.Scatter(
            x=df_state["End Date"],
            y=df_state[metric],
            mode="lines",
            name=metric,
        )
    )

# Update layout for interactivity
fig_all_metrics.update_layout(
    title=f"Weekly Death Trends for All Metrics in {state}",
    xaxis_title="Date",
    yaxis_title="Weekly Death Count",
    xaxis_rangeslider_visible=True,  # Enable range slider
    height=600,
)

# Display the Plotly chart
st.plotly_chart(fig_all_metrics)

# FORECAST SECTION
st.header("Forecast for a Specific Metric")
selected_metric = st.selectbox("Select a Metric", options=metrics)
forecast_steps = st.slider("Select Number of Weeks for Forecast", min_value=1, max_value=52, value=10)

# Prepare the time series data
ts_metric = df_state.set_index("End Date")[selected_metric].dropna()

# Compute Auto ARIMA model only once and store it in session state
if "arima_model" not in st.session_state or st.session_state["arima_metric"] != selected_metric:
    st.session_state["arima_model"] = auto_fit_arima(ts_metric, seasonal=False, alpha=0.05)
    st.session_state["arima_metric"] = selected_metric  # Keep track of the metric for re-computation

# Retrieve the ARIMA model from session state
arima_model = st.session_state["arima_model"]

# Generate the forecast and confidence intervals
forecast_result = arima_model.predict(n_periods=forecast_steps, return_conf_int=True)
forecast_values = forecast_result[0]
forecast_conf_int = forecast_result[1]

# Create forecast index
forecast_index = pd.date_range(start=ts_metric.index[-1] + pd.Timedelta(days=7), periods=forecast_steps, freq="W-SAT")
forecast_series = pd.Series(forecast_values, index=forecast_index)
conf_int_df = pd.DataFrame(
    forecast_conf_int, index=forecast_index, columns=["Lower CI", "Upper CI"]
)

# Plot forecast with confidence intervals
forecast_plot = plot_forecast_with_confidence_intervals_interactive(
    ts=ts_metric,
    forecast=forecast_series,
    conf_int=conf_int_df,
    title=f"Forecast for {selected_metric} in {state}",
    ylabel="Weekly Death Count",
    ylim=(0, None)  # Optional: Set bottom y-axis limit to 0
)

# Display the Plotly chart in Streamlit
st.plotly_chart(forecast_plot)