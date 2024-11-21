import pandas as pd
data = pd.read_csv('UE5-data/data_ehr.csv')
rows, columns = data.shape
print('Rows:', rows, 'Columns:', columns)
threshold = len(data) * 0.30
data_cleaned = data.dropna(axis=1, thresh=threshold)
rows_cleaned, columns_cleaned = data_cleaned.shape
print('Rows_cleaned:', rows_cleaned, 'Columns_cleaned:', columns_cleaned)
print(data_cleaned.info())

