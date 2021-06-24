import os
import pandas as pd


def convert_category_cols_to_str(df):
    """
    Note: This function is particularly useful when writing sav files to parquet

    :param df:  pandas dataframe
    :return: pandas dataframe
    """
    for col in df.columns:
        if type(df[col].dtype) == pd.core.dtypes.dtypes.CategoricalDtype:
            df[col] = df[col].astype(str)

    return df


def drop_cols_containing_str(df, drop_str='Unnamed:'):
    drop_columns = list(filter(lambda k: drop_str in k, df.columns))
    print('columns to drop:', drop_columns)

    return df.drop(drop_columns, axis=1)


def eliminate_null(df):
    null_rows = df.isnull().all(axis=1)
    null_cols = df.isnull().all()
    df.drop(df[null_rows].index,inplace=True)   
    df.columns = df.columns.fillna('to_drop')
    df.drop(columns = list(df.columns[null_cols]),inplace=True)
    return df