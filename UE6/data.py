import pandas as pd

from commons import print_info

DATA_PATH = 'Provisional_COVID-19_Death_Counts_by_Week_Ending_Date_and_State_20241211.csv'


def get_raw_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


def clean_data(df: pd.DataFrame, cols_drop_nan: list[str] = None, cols_fill_nan: list[str] = None) -> pd.DataFrame:
    """
    Clean the data by dropping rows with NaN values in specific columns and filling
    NaN values in other columns with 0. The original DataFrame is not modified.
    :param df:  DataFrame to clean
    :param cols_drop_nan:  Columns to drop the rows for if they contain any NaN values (optional)
    :param cols_fill_nan:  Columns to fill with last known value if they contain NaN values (optional)
    :return:   Cleaned DataFrame
    """
    # Drop rows with NaN in the specified columns
    df_cpy = df.copy()
    if cols_drop_nan is not None:
        initial_row_count = len(df)
        df_cpy = df_cpy.dropna(subset=cols_drop_nan, how='any')
        rows_dropped = initial_row_count - len(df_cpy)
        print_info(f"Dropped {rows_dropped} rows due to NaN in {cols_drop_nan}")

    # Fill NaN values in specific columns with forward fill
    if cols_fill_nan is not None:
        nan_counts_before = df_cpy[cols_fill_nan].isna().sum()
        df_cpy[cols_fill_nan] = df_cpy[cols_fill_nan].ffill()
        for column in cols_fill_nan:
            print_info(f"Filled {nan_counts_before[column]} NaN values in column '{column}'")

    # Convert 'End Date' to datetime and extract the year
    df_cpy['End Date'] = pd.to_datetime(df_cpy['End Date'])
    df_cpy['Year'] = df_cpy['End Date'].dt.year
    df_cpy['Month'] = df_cpy['End Date'].dt.month

    return df_cpy


def filter_data_by_state(df: pd.DataFrame, state: str) -> pd.DataFrame:
    """
    Filter the data for a specific state or the entire U.S.
    :param df: DataFrame to filter
    :param state: Name of the state or 'United States' for national data
    :return: Filtered DataFrame
    """
    if state not in df['State'].unique():
        raise ValueError(f"State '{state}' not found in the data!")
        # Filter for the specified state
    return df[df['State'] == state]



