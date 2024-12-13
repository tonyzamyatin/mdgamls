import pandas as pd
from plotly import graph_objects as go
from plotly.subplots import make_subplots


def plot_trends_interactive(df_state: pd.DataFrame, metrics: list[str], state: str) -> go.Figure:
    """
    Plot weekly death trends of the specified metrics in a given state using Plotly.
    :param df_state:
    :param metrics:
    :param state:
    :return:
    """
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

    return fig_all_metrics


def plot_forecast_with_ci_interactive(
        ts: pd.Series,
        forecast: pd.Series,
        conf_int: pd.DataFrame,
        alpha: float,
        metric: str,
        state: str,
        ylim: tuple = None
):
    """
    Plot time series with forecast and confidence intervals using Plotly.

    :param ts: Actual time series data (pandas Series).
    :param forecast: Forecasted values (pandas Series).
    :param conf_int: Confidence intervals (DataFrame with 'Lower CI' and 'Upper CI').
    :param alpha: Significance level of the computed confidence intervals (default: 0.05).
    :param metric: Metric name.
    :param state: State name.
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

    # Adjust forecast values for display: clamp values below 0 to 0 if ylim[0] is 0
    adjusted_forecast = forecast.clip(lower=0) if ylim and ylim[0] == 0 else forecast

    # Connect the last actual data point to the first forecast point
    extended_forecast_index = [ts.index[-1]] + forecast.index.tolist()
    extended_forecast_values = [ts.values[-1]] + adjusted_forecast.tolist()

    # Add forecast data
    fig.add_trace(
        go.Scatter(
            x=extended_forecast_index,
            y=extended_forecast_values,
            mode="lines",
            name="Forecast",
            line=dict(color="orange"),
            marker={'opacity': 0}  # Suppress markers explicitly
        )
    )

    # Add confidence intervals as an envelope, also adjusting for cutoff
    adjusted_conf_int = conf_int.copy()
    if ylim and ylim[0] == 0:
        adjusted_conf_int["Lower CI"] = adjusted_conf_int["Lower CI"].clip(lower=0)

    fig.add_trace(
        go.Scatter(
            x=forecast.index.tolist() + forecast.index[::-1].tolist(),
            y=adjusted_conf_int["Upper CI"].tolist() + adjusted_conf_int["Lower CI"][::-1].tolist(),
            fill="toself",
            fillcolor="rgba(255, 165, 0, 0.2)",  # Semi-transparent orange
            line=dict(width=0),
            name=f"Confidence Interval α={alpha})",
            hoverinfo="skip",
            marker={'opacity': 0}  # Suppress markers explicitly
        )
    )

    # Update layout
    fig.update_layout(
        title=f"Forecast for {metric} in {state}",
        xaxis_title="Date",
        yaxis_title="Weekly Death Count",
        height=600,
        xaxis_rangeslider_visible=True,
    )

    # Set y-axis limits if specified
    if ylim is not None:
        fig.update_yaxes(range=ylim)

    return fig
