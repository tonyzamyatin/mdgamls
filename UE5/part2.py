import copy
import pandas as pd
from sklearn.cluster import KMeans


def get_numerical_features(data_frame: pd.DataFrame) -> pd.DataFrame:
    """Returns data with only numerical features."""
    data = copy.deepcopy(data_frame)
    data = data.select_dtypes(include=['int64', 'float64'])
    return data.fillna(data.mean())


def elbow_method(data_frame: pd.DataFrame):
    """Returns Array"""
    sum_of_squared_differences = []
    for k in range(1, 15):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(data_frame)
        sum_of_squared_differences.append(kmeans.inertia_)
    return sum_of_squared_differences
