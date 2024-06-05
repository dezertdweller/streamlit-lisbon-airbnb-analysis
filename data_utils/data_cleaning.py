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
    df[price_col] = df[price_col].astype(float).round(3)
    return df

