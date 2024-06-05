import pandas as pd
import numpy as np

def calculate_percentile(df, col, n):
    """
    Calculates the nth percentile of a given numerical column.

    Parameters:
    df: name of the dataframe
    col: name of the column containing numerical data
    n: the nth percentile to be calculated

    returns the nth percentile value for the given column.
    """
    n = n / 100 if n > 1 else n

    percentile_value = df[col].quantile(n)
    print(f"The {col}'s {n}th percentile value is {percentile_value}.")

    return percentile_value

def mean_and_median_compare(df, cat_col, num_col):
    """
    Creates a new dataframe grouping the categorical column of interest and calculates the mean and median value
    of a given numerical column.

    Parameters:
    df: dataframe of interest
    cat_col: column containing categorical data
    num_col: column containing numerical data

    Returns the merged dataframes as a new mean median df.
    """
    col_mean = df.groupby(cat_col)[num_col].mean().round(1).reset_index()
    col_median = df.groupby(cat_col)[num_col].median().round(1).reset_index()
    mean_median_comb = pd.merge(col_mean, col_median, on=cat_col, suffixes=('_mean', '_median'))
    
    return mean_median_comb
    
