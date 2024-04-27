import pandas as pd
import streamlit as st
import plotly.express as px

# create a streamlit function to get Air BNB data
@st.cache
def get_data():
    """
    A function that taks the url for AirBnB data as a 
    variable and reads it into a pandas dataframe.
    """
    url = "https://data.insideairbnb.com/portugal/lisbon/lisbon/2024-03-18/data/listings.csv.gz"
    return pd.read_csv(url)

# use get_data() to get the AirBnB data
df = get_data()