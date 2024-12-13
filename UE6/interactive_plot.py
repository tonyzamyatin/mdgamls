import calendar
import pandas as pd
from matplotlib.colors import to_hex, to_rgb
from plotly import graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


def lighten_color(color, amount=0.5):
    """
    Lighten the given color by mixing it with white.
    :param color: Hex color string or RGB tuple.
    :param amount: Amount to lighten (0.0 = original, 1.0 = white).
    :return: Lightened color in RGB format.
    """
    try:
        c = to_rgb(color)  # Convert to RGB
    except ValueError:
        raise ValueError(f"Invalid color value: {color}")
    return tuple((1 - amount) * channel + amount * 1 for channel in c)


def generate_gradient_with_gaps(primary_color, num_colors):
    """
    Generate a gradient from a lightened version of the primary color to the primary color.
    There is a larger gap for the most primary color.
    :param primary_color: Hex color for the primary color.
    :param num_colors: Number of colors in the gradient.
    :return: List of colors in RGB format.
    """
    light_color = lighten_color(primary_color, amount=0.7)  # Lighten primary color
    base_rgb = to_rgb(primary_color)  # Convert primary color to RGB
    gradient = [
        tuple(
            (1 - i / (num_colors - 2)) * lc + (i / (num_colors - 2)) * bc
            for lc, bc in zip(light_color, base_rgb)
        )
        for i in range(num_colors - 1)
    ]
    # Add a larger gap for the most primary color
    gradient.append(base_rgb)
    return [to_hex(rgb) for rgb in gradient]


def plot_weekly_deaths_by_year(
    df: pd.DataFrame, state: str, metric: str, color_map: dict
) -> go.Figure:
    """
    Plot weekly deaths by year for a specific metric in a given state using Plotly.
    :param df: pandas DataFrame containing the data.
    :param state: State to filter the data for.
    :param metric: Metric to plot.
    :param color_map: Global color map for consistent styling.
    :return: Plotly figure.
    """
    filtered_df = df[df['State'] == state]

    # Drop datetime64 columns to avoid summing issues
    non_datetime_cols = filtered_df.select_dtypes(exclude=['datetime64']).columns
    filtered_df = filtered_df[non_datetime_cols]

    filtered_df = filtered_df.groupby(['Year', 'Month']).sum().reset_index()

    # Determine unique years
    years = sorted(filtered_df['Year'].unique())
    previous_years = years[:-1]  # All years except the most recent

    # Generate gradient for previous years
    gradient_colors = generate_gradient_with_gaps(color_map["primary_color"], len(previous_years))
    custom_colors = gradient_colors + [color_map["accent_color_1"]]

    # Create a Plotly figure
    fig = go.Figure()

    # Add traces for each year with dynamic styling
    for i, year in enumerate(years):
        df_year = filtered_df[filtered_df['Year'] == year]

        fig.add_trace(
            go.Scatter(
                x=df_year['Month'],
                y=df_year[metric],
                mode="lines",
                name=str(year),
                line=dict(color=custom_colors[i])
            )
        )

    # Generate month labels
    months = list(range(1, 13))
    month_labels = [calendar.month_abbr[m] for m in months]  # First three letters of each month

    # Update layout (sort years in legend in descending order, ticks for every month)
    fig.update_layout(
        title=f"Weekly Deaths for {metric} in {state}",
        xaxis_title="Month",
        yaxis_title="Weekly Death Count",
        legend_traceorder="reversed",  # Ensures the legend is in descending order
        height=600,
        xaxis=dict(
            tickmode="array",  # Use custom ticks
            tickvals=months,  # Tick values are months (1-12)
            ticktext=month_labels,  # Tick labels are the abbreviated month names
            tickangle=0,  # Keep month names horizontal
        ),
    )

    return fig


def plot_relative_death_counts(df: pd.DataFrame, year: int, month: int, states: list[str], metrics: list[str], color_map: dict) -> go.Figure:
    """
    Plot relative death counts by metric for a specific month and year using Plotly.
    :param df: pandas DataFrame containing the data.
    :param year: the year to filter the data for.
    :param month: the month to filter the data for.
    :param states: the states to filter the data for.
    :param metrics: the metrics to plot.
    :param color_map: Global color map for consistent styling.
    :return: Plotly figure.
    """
    filtered_df = df[(df['Year'] == year) & (df['Month'] == month) & (df['State'].isin(states))]
    relative_df = filtered_df.melt(
        id_vars=['State'],
        value_vars=metrics,
        var_name='Metric',
        value_name='Deaths'
    )
    relative_df = relative_df.merge(
        filtered_df[['State', 'Total']], on='State'
    )
    relative_df['Relative Deaths'] = relative_df['Deaths'] / relative_df['Total']

    fig = px.bar(
        relative_df,
        x='State',
        y='Relative Deaths',
        color='Metric',
        color_discrete_map=color_map["metric_colors"],
        title=f"Relative Death Counts by Metric ({month}/{year})",
        labels={'Relative Deaths': '% of Total Deaths'}
    )
    fig.update_layout(barmode='stack')
    return fig


def plot_trends(df_state: pd.DataFrame, metrics: list[str], state: str, color_map: dict) -> go.Figure:
    """
    Plot weekly death trends of the specified metrics in a given state using Plotly.
    :param df_state: DataFrame containing the data for the specified state.
    :param metrics: List of metrics to plot.
    :param state: Name of the state.
    :param color_map: Global color map for consistent styling.
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
                line=dict(color=color_map["metric_colors"][metric])
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


def plot_forecast_with_ci(
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
