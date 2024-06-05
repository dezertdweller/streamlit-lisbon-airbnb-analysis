import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
import data_utils.data_utils as du
from config import IMAGE_PATH
import data_utils.data_cleaning as dc

st.title("Lisbon AirBnB Market Analysis")
st.markdown("""Welcome to this in-depth analysis of 2024 AirBnB listing data in Lisbon, Portugal.
            I'll be using Streamlit and Plotly to analyze and visualize data.
            
            """)
st.header("A little history")
st.markdown("""Lisbon, or Lisboa in Portuguese, is a city known for its charm [...]
            more stuff here.""")

st.header("Project Overview")
st.markdown("""My aim with this project is to provide analysis on the Lisbon AirBnB market for a 
            new business in the greater Lisbon area. The client, Quinta Nere Maitia, is opening
            10 tiny homes on a property just outside of Lisbon. This quiet refuge aims to provide
            a luxurious home away from home experience for those interested in relaxation and 
            exciting tourism opportunities. 
            """)
st.subheader("**Quinta Nere Maitia**")
st.image(IMAGE_PATH + 'quinta-1.jpeg')

# import Lisbon airbnb data into a new dataframe
# create a streamlit function to get Air BNB data
st.subheader("Sourcing data")
st.markdown("""For this project, I'll be sorucing data from [Inside AirBnB](https://insideairbnb.com).
            ...""")

st.markdown("**Importing Data**")
with st.echo():
    @st.cache_data
    def get_data():
        """
        A function that taks the url for AirBnB data as a 
        variable and reads it into a pandas dataframe.
        """
        url = "https://data.insideairbnb.com/portugal/lisbon/lisbon/2024-03-18/data/listings.csv.gz"
        return pd.read_csv(url, dtype={'id': str})

# create a new dataframe containing lisbon data    
df = get_data()

# convert price column to floats
dc.convert_price_to_float(df,price_col='price')

# drop rows with missing price data
df = df.dropna(axis=0, subset=['price'])

# display first 10 rows of data
st.subheader("Full dataframe limited to 10 entries")
st.dataframe(df.head(10))

# display map of locations
st.header("Initial Look at AirBnB Locations in Lisbon")
st.map(df, color='#0C9B98')

# create some columns to filter the dataframe by in an interactive way
standard_columns = ["name", "host_name", "neighbourhood_cleansed", "room_type", "price"]

# create a dataframe view that filters with the standard column names
cols_simple = st.multiselect("Columns", df.columns.tolist(), default=standard_columns)
st.dataframe(df[cols_simple])

# most expensive airbnbs and their locations on the map
st.header("Top 1% Most Expensive AirBnB Locations and Prices")
st.markdown("""
            Some text here to explain the map and table.""")
top_1_perc = du.calculate_percentile(df, 'price', 0.99)
st.map(df.query("price >= @top_1_perc")[["latitude", "longitude"]])
most_exp_listings = df[df['price'] >= top_1_perc].sort_values('price', ascending=False)
st.dataframe(most_exp_listings[cols_simple])

# price distribution excluing top 5% most expensive listings
st.header("Lisbon AirBnB Price Distribution Excluding Top 5%")
st.markdown("""
            Some text here to explain the graph.""")
top_5_perc = du.calculate_percentile(df, 'price', 0.95)
df_price_limit = df[df['price'] <= top_5_perc]
fig_price_dist = px.histogram(df_price_limit, x="price")
st.plotly_chart(fig_price_dist, use_container_width=True)

# compare mean and median prices
st.header("Average and Median Prices for AirBnB's in Lisbon")
st.markdown("""
            Some text here to explain the graph.""")
# limited price df mean and median prices per night
st.subheader('Mean and Median Prices Per Night Excluding Most Expensive Stays')
mean_med_price_limit = du.mean_and_median_compare(df_price_limit, 'room_type', 'price')
st.table(mean_med_price_limit)

# full df mean and median prices per night
st.subheader('Mean and Median Prices Per Night for All Stays')
mean_med_price = du.mean_and_median_compare(df, 'room_type', 'price')
st.table(mean_med_price)