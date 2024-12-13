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
        total_sum = state_df['Total Deaths'].sum()
        state_sums[state] = {'COVID-19': covid_sum,
                             'COVID-19 Percentage': (covid_sum / total_sum) * 100,
                             'Influenza': influenza_sum,
                             'Influenza Percentage':(influenza_sum / total_sum) * 100,
                             'Pneumonia': pneumonia_sum,
                             'Pneumonia Percentage': (pneumonia_sum / total_sum) * 100}
    sorted_state_sums = {state: state_sums[state] for state in sorted(state_sums)}
    df_state_sums = pd.DataFrame(sorted_state_sums).T.reset_index()
    df_state_sums = df_state_sums.rename(columns={'index': 'State'})
    df_melted = df_state_sums.melt(id_vars='State', var_name='Category', value_name='Number')
    df_melted['Type'] = df_melted['Category'].apply(lambda x: 'Percentage' if 'Percentage' in x else 'Deaths')
    return df_melted

def plot_comparison(df, year, month):
    plt.figure(figsize=(10, 6))
    df_number = df[df['Type'] == 'Deaths']
    sns.barplot(data=df_number, x='Category', y='Number', hue='State', palette='Set2')
    df_percentage = df[df['Type'] == 'Percentage'].sort_values(by=['State']).reset_index(drop=True)
    percentage = df_percentage['Number'].tolist()
    all_bars = [bar for container in plt.gca().containers for bar in container]
    for bar, percentage in zip(all_bars, percentage):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 5,
            str(round(percentage,2)) + "%",
            ha='center', va='bottom', fontsize=10, color='black'
        )
    plt.title(f"Comparison of Deaths by Category Across States in {str(month) + '/' if month != 'No month selected' else ''}{year}")
    plt.ylabel('Number of Deaths')
    plt.xlabel('Cause of Death')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(title='State')

    return plt
