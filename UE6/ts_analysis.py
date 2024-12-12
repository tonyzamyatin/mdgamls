import pandas as pd
import pmdarima as pm
import plotly.graph_objects as go
from matplotlib import ticker as mtick, pyplot as plt
from statsmodels.tsa.arima.model import ARIMA, ARIMAResults
from statsmodels.tsa.seasonal import DecomposeResult, seasonal_decompose
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller

from data import filter_data_by_state


def create_multi_time_series(df: pd.DataFrame, metrics=list[str], state: str = 'United States') -> pd.DataFrame:
    """
    Create a multi time series DataFrame for the specified state for containing a time series for each metric.
    :param df: Cleaned DataFrame
    :param metrics: List of metrics to analyze
    :param state: Name of the state to analyze
    :return: Multi time series DataFrame
    """
    # Filter the data for the specified state
    state_data = filter_data_by_state(df, state)

    # Validation: Ensure only one data point per End Date
    duplicates = state_data.duplicated(subset=['End Date'], keep=False)
    assert not duplicates.any(), (
        f"Data for state '{state}' contains multiple entries for the same End Date: "
        f"{state_data[duplicates]}"
    )

    # Group the data by 'End Date' and sum the weekly death counts
    multi_time_series = state_data.set_index('End Date')[metrics].sort_index()

    return multi_time_series


def plot_trend(multi_ts: pd.DataFrame, state: str = 'United States'):
    """
    Analyze trends for a specific state. If not state is specified the national data is analyzed.
    Conditionally scales the y-axis to thousands if values are large.
    :param multi_ts: Multi time series DataFrame
    :param state: Name of the state to analyze
    """
    # Determine if scaling is needed (if max value > 1000)
    max_value = multi_ts.max().max()
    scale_to_thousands = max_value > 1000
    scaling_factor = 1000 if scale_to_thousands else 1
    y_label = "Weekly Death Count (in thousands)" if scale_to_thousands else "Weekly Death Count"

    # Plot trends for each metric
    ax = multi_ts.div(scaling_factor).plot(figsize=(12, 6), title=f"{state} Trends in Weekly Death Counts")
    ax.set_ylabel(y_label)
    ax.set_xlabel("Date")

    # Format y-axis to show values in thousands if scaled
    if scale_to_thousands:
        ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x:.0f}k'))

    plt.legend(title="Metrics")
    plt.show()


def decompose_timeseries(ts: pd.DataFrame) -> DecomposeResult:
    """
    Decompose the time series into trend, seasonal, and residual components, and plot the decomposition.
    :param ts: Time series DataFrame
    :return: Decomposition result
    """
    # Perform time series decomposition
    decomposition = seasonal_decompose(ts, model='additive', period=52)

    # Plot the decomposition
    fig = decomposition.plot()
    fig.set_size_inches(12, 8)  # Increase the figure size

    # Adjust layout for better spacing
    plt.subplots_adjust(hspace=0.5)  # Add vertical space between subplots

    # Improve x-axis readability
    for ax in fig.axes:
        ax.tick_params(axis='x', rotation=45)  # Rotate x-axis labels

    plt.show()

    return decomposition


def perform_adf(ts: pd.DataFrame) -> None:
    """
    Test the time series for stationary using the ADF test.
    :param ts: Time series DataFrame to test for stationary
    :return:
    """
    adf_result = adfuller(ts)
    print(f"ADF Statistic: {adf_result[0]}")
    print(f"p-value: {adf_result[1]}")
    if adf_result[1] < 0.05:
        print(f"The time series for is stationary.")
    else:
        print(f"The time series for is not stationary.")


def fit_arima(ts: pd.DataFrame, order=tuple[int, int, int]) -> ARIMAResults:
    """
    Fit an ARIMA model to the time series data.
    :param ts: Time series data (pandas DataFrame).
    :param order: ARIMA order (p, d, q).
    :return: Resulting ARIMA model.
    """
    model = ARIMA(ts, order=order)
    result = model.fit()

    print(result.summary())

    return result


def fit_sarima(ts: pd.DataFrame, order=tuple[int, int, int, int]) -> ARIMAResults:
    """
    Fit a SARIMA model to the time series data.
    :param ts: Time series data (pandas DataFrame).
    :param order: SARIMA order (p, d, q, s).
    :return: Resulting SARIMA model.
    """
    model = SARIMAX(
        ts,
        order=order[:3],
        seasonal_order=order,
        enforce_stationarity=False,
        enforce_invertibility=False
    )
    result = model.fit()

    print(result.summary())

    return result


def plot_forecast_with_confidence_intervals(
        ts: pd.Series,
        forecast: pd.Series,
        conf_int: pd.DataFrame,
        title: str,
        ylabel: str = "Values",
        xlabel: str = "Date",
        ylim: tuple = None
):
    """
    Plot time series with forecast and confidence intervals.

    :param ts: Actual time series data (pandas Series).
    :param forecast: Forecasted values (pandas Series).
    :param conf_int: Confidence intervals (DataFrame with 'Lower CI' and 'Upper CI').
    :param title: Title of the plot.
    :param ylabel: Y-axis label.
    :param xlabel: X-axis label.
    :param ylim: Y-axis limits (optional).
    """
    plt.figure(figsize=(12, 6))
    plt.plot(ts, label="Actual Data", color="blue")
    plt.plot(forecast, label="Forecast", linestyle="--", color="orange")
    plt.fill_between(
        forecast.index,
        conf_int.iloc[:, 0],
        conf_int.iloc[:, 1],
        color="orange",
        alpha=0.3,
        label="Confidence Interval"
    )
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if ylim is not None:
        plt.ylim(ylim)
    plt.legend()
    plt.show()


def auto_fit_arima(ts: pd.Series, seasonal: bool, alpha: float, ic: str = 'aic') -> list:
    """
    Automatically fits the best ARIMA model to the time series data.
    :param ts: Time series data (pandas Series).
    :param seasonal: Whether the data is seasonal.
    :param alpha: Significance level for the confidence intervals.
    :param ic: Information criterion to use ('aic' or 'bic').
    :return: pmdarima ARIMA model.
    """
    model = pm.auto_arima(
        ts,
        seasonal=seasonal,
        trace=True,  # Print fitting progress
        alpha=alpha,
        information_criterion=ic,
        error_action="ignore",  # Ignore orders that don't converge
        suppress_warnings=True  # Suppress convergence warnings
    )
    print(model.summary())
    return model


def analyze_residuals(model: ARIMAResults) -> None:
    """
    Analyze the residuals of the ARIMA model.
    :param model: ARIMA model.
    """
    residuals = model.resid
    plt.figure(figsize=(12, 6))
    plt.plot(residuals, color="blue")
    plt.title("Residuals of ARIMA Model")
    plt.xlabel("Date")
    plt.ylabel("Residuals")
    plt.axhline(y=0, color="red", linestyle="--")
    plt.show()

    print("Residuals Statistics:")
    print(residuals.describe())

    # Test for autocorrelation in residuals
    from statsmodels.graphics.tsaplots import plot_acf
    plot_acf(residuals, lags=30)
    plt.show()

    # Residuals histogram
    residuals.plot(kind='hist', bins=30, title="Residual Histogram - (2, 1, 3)")
    plt.show()

    # Test for normality of residuals
    from scipy.stats import shapiro
    _, p_value = shapiro(residuals)
    print(f"Shapiro-Wilk test p-value: {p_value}")
    if p_value > 0.05:
        print("Residuals are normally distributed.")
    else:
        print("Residuals are not normally distributed.")


def plot_forecast_with_confidence_intervals_interactive(
        ts: pd.Series,
        forecast: pd.Series,
        conf_int: pd.DataFrame,
        title: str,
        ylabel: str = "Values",
        xlabel: str = "Date",
        ylim: tuple = None
):
    """
    Plot time series with forecast and confidence intervals using Plotly.

    :param ts: Actual time series data (pandas Series).
    :param forecast: Forecasted values (pandas Series).
    :param conf_int: Confidence intervals (DataFrame with 'Lower CI' and 'Upper CI').
    :param title: Title of the plot.
    :param ylabel: Y-axis label.
    :param xlabel: X-axis label.
    :param ylim: Y-axis limits (optional).
    """
    # Create the figure
    fig = go.Figure()

    # Add actual data
    fig.add_trace(
        go.Scatter(
            x=ts.index,
            y=ts.values,
            mode="lines",
            name="Actual Data",
            line=dict(color="blue"),
        )
    )

    # Add forecast data
    fig.add_trace(
        go.Scatter(
            x=forecast.index,
            y=forecast.values,
            mode="lines",
            name="Forecast",
            line=dict(color="orange", dash="dash"),
        )
    )

    # Add confidence intervals as an envelope
    fig.add_trace(
        go.Scatter(
            x=forecast.index.tolist() + forecast.index[::-1].tolist(),
            y=conf_int["Upper CI"].tolist() + conf_int["Lower CI"][::-1].tolist(),
            fill="toself",
            fillcolor="rgba(255, 165, 0, 0.2)",  # Semi-transparent orange
            line=dict(width=0),
            name="Confidence Interval",
            hoverinfo="skip",
        )
    )

    # Update layout
    fig.update_layout(
        title=title,
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        height=600,
        xaxis_rangeslider_visible=True,
    )

    # Set y-axis limits if specified
    if ylim is not None:
        fig.update_yaxes(range=ylim)

    return fig
