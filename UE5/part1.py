from pathlib import Path

import pandas as pd


def read_csv(file: Path) -> pd.DataFrame:
    """Reads data from a csv file and returns the data as a Pandas dataframe"""
    # TODO: Implement


def clean_data(data_frame: pd.DataFrame) -> pd.DataFrame:
    """Returns a clean copy of the data frame"""
    # TODO: Implement, use copy.deepcopy to first copy the dataframe before cleaning as not to overwrite the original data

data = pd.read_csv('UE5-data/data_ehr.csv')
rows, columns = data.shape
print('Rows:', rows, 'Columns:', columns)
threshold = len(data) * 0.30
data_cleaned = data.dropna(axis=1, thresh=threshold)
rows_cleaned, columns_cleaned = data_cleaned.shape
print('Rows_cleaned:', rows_cleaned, 'Columns_cleaned:', columns_cleaned)
print(data_cleaned.info())
