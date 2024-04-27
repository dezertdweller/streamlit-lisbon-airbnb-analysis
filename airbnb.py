import pandas as pd
import streamlit as st
import plotly.express as px

# create a streamlit function to get Air BNB data
@st.cache_data
def get_data():
    """
    A function that taks the url for AirBnB data as a 
    variable and reads it into a pandas dataframe.
    """
    url = "https://data.insideairbnb.com/portugal/lisbon/lisbon/2024-03-18/data/listings.csv.gz"
    return pd.read_csv(url, dtype={'id': str})

# use get_data() to get the AirBnB data
df = get_data()

st.title("Streamlit 101: An in-depth introduction")
st.markdown("Welcome to this in-depth introduction to [...].")
st.header("Customary quote")
st.markdown("> I just love to go home, no matter where I am [...]")

st.code("""
@st.cache_data
def get_data():
    url = "https://data.insideairbnb.com/portugal/lisbon/lisbon/2024-03-18/data/listings.csv.gz"
    return pd.read_csv(url)
""", language="python")

st.dataframe(df.head(15))