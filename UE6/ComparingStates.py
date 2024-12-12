import pandas as pd
import seaborn as sns

from matplotlib import pyplot as plt
from FilteringTrends import extract_month


def filter_sum(df, year, states, month):
    df_filtered = df[df['Year'] == year]

    if month != 'No month selected':
        df_filtered['New Month'] = df_filtered['End Date'].apply(extract_month)
        df_filtered = df_filtered[df_filtered['New Month'] == month]

    state_sums = {}

    for state in states:
        state_df = df_filtered[df_filtered['State'] == state]
        covid_sum = state_df['COVID-19 Deaths'].sum()
        pneumonia_sum = state_df['Pneumonia Deaths'].sum()
        influenza_sum = state_df['Influenza Deaths'].sum()
        state_sums[state] = {'COVID-19 Deaths': covid_sum,
                             'Pneumonia Deaths': pneumonia_sum,
                             'Influenza Deaths': influenza_sum}

    df_state_sums = pd.DataFrame(state_sums).T.reset_index()
    df_state_sums = df_state_sums.rename(columns={'index': 'State'})
    df_melted = df_state_sums.melt(id_vars='State', var_name='Category', value_name='Deaths')
    return df_melted

def plot_comparison(df, year, month):

    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='Category', y='Deaths', hue='State', palette='Set2')
    plt.title(f"Comparison of Deaths by Category Across States in {str(month) + '/' if month != 'No month selected' else ''}{year}")
    plt.ylabel('Number of Deaths')
    plt.xlabel('Death Category')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(title='State')

    return plt
