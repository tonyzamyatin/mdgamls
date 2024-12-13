<h1 style="text-align:center;">Report: Interactive Visual Analytics System</h1>

<p style="text-align:center;">by Anton Zamyatin & Hannah Teis</p>

## Dataset
The chosen dataset 'Provisional COVID-19 Death Counts by Week Ending Date and State' gives information to 
COVID-19-related deaths reported weekly across U.S. states since 2020, including deaths involving pneumonia and influenza. 
It was downloaded from the [Centers for Disease Control and Prevention (CDC)](https://data.cdc.gov/NCHS/Provisional-COVID-19-Death-Counts-by-Week-Ending-D/r8kw-7aab/about_data). 
The dataset includes 17 columns and ~17.5k rows, each of which represents deaths related to COVID-19, pneumonia, influenza by week and state. 
It follows that there are ~297500 entries. The key attributes include temporal information (Start Date, End Date, Year,...), geographical information (State),
cause of death (COVID-19, Pneumonia, Influenza, and Combined), total number of deaths. This dataset is of interest because it gives a
comprehensive overview of the impact of a pandemic (Corona Virus) over time in multiply locations (States) with different healthcare policies. 
These properties make it ideal to compare death statistics between states or time periods, identify peaks or other anomalies and identify correlations.  

## Users
The intended users of the interactive visual analytics system are policymakers and their epidemiologist consultants. 
The system is designed to address the challenges of monitoring dynamic trends in disease-related mortality, enabling users to stay informed about evolving patterns in health data.
A key benefit of the system is the basis it builds to support decision-making for effective allocation of limited resources across regions and aid in preparation for seasonal spikes in disease incidence. 
By providing comprehensive analytical tools, the system empowers users to design evidence-based policies and evaluate their impact.
Additionally, the system equips public health officials to proactively address emerging public health crises instrumental by anticipating future trends.

## Tasks
The interactive visual analytics system implements tools to compare epidemiological death statistics across states and years, 
follow trends and make predictions based on them. For effectively comparing the data, filter options are available. 

## Technologies
The interactive visual analytics system is a webapp programmed in python with the open-source library Streamlit in the IDE Pycharm. Other libraries used were Pandas for working with dataset, Plotly for interactive graphs and 
Pmdarima for time series analysis. The version control was managed in Github. Streamlit has been reported to malfunction with Safari, but should work with the browsers Google Chrome, Firefox, or Microsoft Edge. 

## Implementation
To tackle the identified challenges of the users and defined tasks four interactive visual analytics features have been implemented: 
1. Comparing Weekly Death Trends across Years
2. Following Weekly Death Trends by State
3. Comparing Weekly Death Trends across States
4. Predicting for a Cause of Death

### Comparing Weekly Death Trends across Years
This feature, located at the top-left corner, presents a line graph visualizing annual death trends. 
The x-axis displays months within a year, while the y-axis represents the weekly number of deaths. 
Each line corresponds to the progression of pathogen-related deaths for a specific year (2020–2024), with the most recent year, 2024, prominently highlighted in green for easy identification.

Above the graph, users can refine the displayed data through two filter options:
1. State Dropdown: The user can choose the state for which the death trends will be plotted.
2. Pathogen Dropdown: The user can select the cause of death, including options such as COVID-19, Pneumonia, Influenza, or Pneumonia & COVID-19 (logical &).

### Following Weekly Death Trends by State
This feature, located in the top-right section of the interface, provides a detailed visualization of weekly deaths over time with a line plot.
The x-axis represents time, while the y-axis represents the weekly number of deaths. 
Each line on the graph depicts the trends for a specific cause of death, including COVID-19, Pneumonia, Influenza, and a combined category for Pneumonia & COVID-19.

For this feature there are two filtering options as well:
1. State Dropdown: The user can choose the state for which the death trends will be plotted. 
This selection also determines the state for the "Predicting for a Cause of Death" feature below.
2. Time Interval Filtering: Beneath the graph, a slider element allows users to refine the displayed time interval

### Comparing Weekly Death Trends across States
This feature, located in the bottom-left section, allows users to analyze pathogen-related deaths across states. 
Upon selecting a state from the dropdown menu, a bar plot is displayed. The x-axis represents selected states, while the y-axis shows 
the percentage of pathogen-related deaths relative to all deaths in each state for a specified time period.
Each bar is segmented into four distinct colors, representing deaths caused by COVID-19, Pneumonia, Influenza, and Pneumonia & COVID-19 combined.
Users can compare data by selecting up to five states and specifying the time period above the plot. If all options are deselected, the plot will automatically disappear.

The interactive aspect here is filtering:
1. State Multiselect: The user can choose the state for which the % of pathogen related deaths will be compared. 
2. Time Dropdowns: The user can select a specific year and month.

### Predicting for a Cause of Death
This feature, located in the bottom-right corner, provides a forecast function computed using the ARIMA model with a 95% confidence interval and is based on the last known data point of the state selected in 'Following Weekly Death Trends by State'.
The historical data is depicted in blue, showcasing weekly fluctuations over time. The orange line shows the trend, that is predicted for the specified number of weeks. 
A yellow translucent band represents the uncertainty of the predictions, giving users a clear visual cue about the confidence range.

This feature allows for modifications in three aspects:
1. Pathogen Dropdown: The user can select which pathogen to predict the number of deaths to. 
2. Week Slider: The user can choose how many weeks into the future they want the prediction to be made (max 52 weeks).
3. Time Interval Filtering: Beneath the graph, a slider element allows users to refine the displayed time interval

## Insights
The "Comparing Weekly Death Trends Across Years" feature highlights a clear decline in deaths related to COVID-19 and Pneumonia since 2022/2023.
The "Following Weekly Death Trends by State" feature reveals significant waves of COVID-19 and Pneumonia-related deaths in January 2021 and 2022, pointing to critical phases in the pandemic. 
Also peaks in winter can be observed suggesting a seasonal pattern of rising deaths during winter months.
Predictions for Pneumonia-related deaths in the U.S. indicate the potential for increases during January-March, warranting close monitoring.
Additionally, exploratory analysis in analysis.ipynb suggests a correlation between Pneumonia and COVID-19 deaths (co-morbidity). 
This hypothesis is supported by synchronized rising trends identified in the system’s visual analysis.

