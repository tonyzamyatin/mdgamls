from datetime import datetime

from matplotlib import pyplot as plt


def filter_data(df, year, state):
    df_filtered = df[(df['Year'] == year) & (df['State'] == state)]

    def extract_month(ts):
        date = datetime.strptime(ts, '%m/%d/%Y')
        return date.month

    df_filtered['New Month'] = df_filtered['End Date'].apply(extract_month)

    grouped_df = df_filtered.groupby('New Month').agg({
        'COVID-19 Deaths': 'sum',
        'Pneumonia Deaths': 'sum',
        'Influenza Deaths': 'sum'
    }).reset_index()

    return grouped_df


def plot_trend(df, state, year):
    plt.figure(figsize=(12, 6))
    plt.plot(df['New Month'], df['COVID-19 Deaths'], label='COVID-19 Deaths', marker='o')
    plt.plot(df['New Month'], df['Influenza Deaths'], label='Influenza Deaths', marker='x')
    plt.plot(df['New Month'], df['Pneumonia Deaths'], label='Pneumonia Deaths', marker='s')

    plt.title('Weekly Deaths in ' + state + ' in ' + year)
    plt.xlabel('Month')
    plt.ylabel('Number of Deaths')
    plt.legend()
    plt.grid()

    return plt