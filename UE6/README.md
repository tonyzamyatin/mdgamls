# Report: Interactive Visual Analytics System
<p style="text-align:center;">by Anton Zamyatin & Hannah Teis</p>

## Dataset
The chosen dataset 'Provisional COVID-19 Death Counts by Week Ending Date and State' gives information to 
COVID-19-related deaths reported weekly across U.S. states since 2020, including deaths involving pneumonia and influenza. 
It was downloaded from the [Centers for Disease Control and Prevention (CDC)](https://data.cdc.gov/NCHS/Provisional-COVID-19-Death-Counts-by-Week-Ending-D/r8kw-7aab/about_data). 
The dataset includes 17 columns and 17.5k rows, each of which represents deaths related to COVID-19, pneumonia, influenza by week and state. 
It follows that there are 297500 entries. The key attributes include temporal information (Start Date, End Date, Year,...), geographical information (State),
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
The interactive visual analytics system implements tools to compare epidemiological death statistics across states and seasons, identify trends and make predictions based on them.

## User Manual

1. Write all the code in python scripts and functions
2. Call functions with in Jupyter notebook with constants
   (defined somewhere visible so that can be changed seamlessly)
3. Add real interactive visualization (if time allows)