import copy
import pandas as pd


def read_csv(file: str) -> pd.DataFrame:
    """Reads data from a csv file and returns the data as a Pandas dataframe"""
    return pd.read_csv(file)


def clean_data(data_frame: pd.DataFrame) -> pd.DataFrame:
    """Returns a clean copy of the data frame"""
    data_copy = copy.deepcopy(data_frame)
    thresh = len(data_copy) * 0.30
    thresh = int(thresh)
    return data_copy.dropna(axis=1, thresh=thresh)
