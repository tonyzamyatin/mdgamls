import streamlit as st
import pandas as pd
from data import get_cleaned_and_sorted_data
from ts_analysis import auto_fit_arima
from interactive_plot import plot_trends, plot_forecast_with_ci, plot_weekly_deaths_by_year, plot_relative_death_counts

# ================== LOAD DATA ==================
df = get_cleaned_and_sorted_data()

# ================== SETTINGS ===================
METRICS = [
        "COVID-19",
        "Pneumonia & COVID-19",
        "Pneumonia",
        "Influenza"
    ]

# Global color map for consistent styling
COLOR_MAP = {
    "primary_color": "#FF69B4",  # Bright pink
    "accent_color_1": "#00FF00",  # Bright green
    "accent_color_2": "#1E90FF",  # Dodger blue
    "metric_colors": {
        "COVID-19": "#FF7F50",  # Coral
        "Pneumonia": "#FFD700",  # Golden yellow
        "Influenza": "#87CEFA",  # Light blue
        "Pneumonia & COVID-19": "#FFA500",  # Orange (lighter and more distinct from COVID-19)
    }
}

CI_ALPHA = 0.05

# ================ STREAMLIT APP ================
st.set_page_config(layout="wide")
# TECHNICAL NOTES
st.sidebar.markdown(
    """
    # USER INFORMATION
    ## Data    
    Last updated: December 11, 2024
    
    The data is sourced from the CDC's official
    ["Provisional COVID-19 Death Counts by Week Ending Date and State"](https://data.cdc.gov/NCHS/Provisional-COVID-19-Death-Counts-by-Week-Ending-D/r8kw-7aab/about_data) dataset.

    ## Technical Notes
    The time series is fitted using an Auto ARIMA model with seasonal component.
    
    The forecast is computed using the ARIMA model with a 95% confidence interval and is based on the last known data point and extends into the 
    future.
    
    For more details please refer to the technical documentation.
    
    # DISCLAIMER
    1. Death counts shown here may differ from other published sources, as data currently are lagged by an average of 1–2 weeks.
    2. Forecasting models are subject to uncertainty and may not always be accurate.
    """
)

# TITLE AND DESCRIPTION
st.title('Visual Analysis of COVID-19, Pneumonia, and Influenza Deaths in the U.S.')

# Add custom CSS for padding/margin between columns
st.markdown(
    """
    <style>
    .block-container {
        padding: 1em 2em; /* Adjust these values for desired spacing */
    }
    .stVertical {
        margin-left: 2em; /* Add margin between the two columns */
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Layout: Two Columns
col1, col2 = st.columns([1, 1], gap="large")

# LEFT COLUMN
with col1:
    # Section 1: Line chart
    st.header("Weekly Death Trends across Years")
    # Create two columns for the side-by-side layout
    col_state, col_metric = st.columns(2)
    # Add the selectbox widgets in each column
    with col_state:
        selected_state = st.selectbox("Select a State:", options=df['State'].unique())
    with col_metric:
        selected_metric = st.selectbox("Select a Metric:", options=METRICS)
    line_chart_fig = plot_weekly_deaths_by_year(df, selected_state, selected_metric, COLOR_MAP)
    st.plotly_chart(line_chart_fig, use_container_width=True)

    # Section 2: Relative death counts
    st.header("Relative Death Counts across States")
    col_year, col_month = st.columns(2)
    # Add the selectbox widgets in each column
    with col_year:
        selected_year = st.selectbox("Select a Year:", options=sorted(df['Year'].unique(), reverse=True))
    with col_month:
        selected_month = st.selectbox("Select a Month:", options=range(1, 13))

    selected_states = st.multiselect("Select up to 5 States:", options=df['State'].unique(), max_selections=5)
    st.markdown(
        """
        <style>
        .custom-margin {
            margin-bottom: 1em; /* Adjust this value for desired spacing */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    if selected_states:
        bar_chart_fig = plot_relative_death_counts(df, selected_year, selected_month, selected_states, METRICS, COLOR_MAP)
        st.plotly_chart(bar_chart_fig, use_container_width=True)

# RIGHT COLUMN
with col2:
    st.header(f"Weekly Death Trends by State")
    state = st.selectbox("Select a State", options=df['State'].unique())

    # Filter data for the selected state
    df_state = df[df['State'] == state]

    # Plot all metrics for the selected state
    fig_all_metrics = plot_trends(df_state, METRICS, state, COLOR_MAP)
    st.plotly_chart(fig_all_metrics)

    # FORECAST SECTION

    st.header("Forecast for a Specific Metric")
    selected_metric = st.selectbox("Select a Metric", options=METRICS)
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
    forecast_plot = plot_forecast_with_ci(timeseries, forecast_series, conf_int_df, CI_ALPHA, selected_metric, state, ylim=(0, None))
    st.plotly_chart(forecast_plot)
