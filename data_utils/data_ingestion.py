import pandas as pd
import streamlit as st
import plotly.express as px

# create a streamlit function to get Air BNB data
with st.echo():
    @st.cache_data
    def get_data():
        """
        A function that taks the url for AirBnB data as a 
        variable and reads it into a pandas dataframe.
        """
        url = "https://data.insideairbnb.com/portugal/lisbon/lisbon/2024-03-18/data/listings.csv.gz"
        return pd.read_csv(url, dtype={'id': str})