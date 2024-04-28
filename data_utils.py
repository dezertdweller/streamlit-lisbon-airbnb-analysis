import pandas as pd
import numpy as np

def convert_price_to_float(df, price_col):
    """
    Converts a dataframe column containing price data as strings into floats.
    
    Parameters:
    df: name of the dataframe.
    price_col: name of the price column to convert. 
    
    Note:
    Price column data should be a string in this general format: $1,000.00. 
    It will remove the dollar sign and commas before converting the number 
    to a float.
    """
    # remove $ and , from values
    df[price_col] = df[price_col].str.replace('$', '').str.replace(',', '')
    # convert to float
    df[price_col] = df[price_col].astype(float)
    return df

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
    
    print("The {col}'s {n}th percentile value is {percentile_value}.")

    return percentile_value
