import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
import seaborn as sns
import data_utils.data_utils as du
from config import IMAGE_PATH
import matplotlib.colors as mcolors
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
            The most expensive AirBnBs in Lisbon are concentrated near the coastline.
            The prices range from \$800 to \$9,200 per night.""")
top_1_perc = du.calculate_percentile(df, 'price', 0.99)
st.map(df.query("price >= @top_1_perc")[["latitude", "longitude"]], color='#0C9B98')

# top 5 most expensive listings details
st.subheader('Details About the 5 Most Expensive Listings')
most_exp_listings = df[df['price'] >= top_1_perc].sort_values('price', ascending=False)
st.dataframe(most_exp_listings[['name', 'host_name', 'price', 'accommodates', 'bedrooms']].head(5))

# most expensive listings grouped by price
st.subheader('Price Ranges for Top 1% Most Expensive Listings')
bins = [799, 1200, 3000, 5000, 7000, 10000]
labels = ['799 - 1,199', '1,200 to 2,999', '3,000 - 4,999', '5,000 - 6,999', '7,000+']
most_exp_listings['cost_range'] = pd.cut(most_exp_listings['price'], bins=bins, labels=labels, right=False)
expensive_categories = most_exp_listings.groupby('cost_range')['id'].count().reset_index()
expensive_categories.columns = ['Cost Per Night', 'Count of Listings']
st.dataframe(expensive_categories)

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

# neighboord and room price analysis
st.header('Price Variation by Neighborhood and by Average Number of Rooms')
st.markdown("""
            Some text here to analyze chart and map.""")
# create new df excluding hotels 
df_no_hotels = df.drop(df[df['bedrooms'] >= 20].index)
# create new mean median price compare for each neighborhood
df_neighbourhoods = du.mean_and_median_compare(df_no_hotels, 'neighbourhood_group_cleansed', 'price')
# calculate avg bedrooms per neighborhood
df_neighbourhoods_rooms = df_no_hotels.groupby('neighbourhood_group_cleansed')['bedrooms'].mean().round(1).reset_index()
# merge new neighbourhood dfs
df_avg_room_price = pd.merge(df_neighbourhoods, df_neighbourhoods_rooms, on='neighbourhood_group_cleansed')
# calculate average price per room for each neighborhood
df_avg_room_price['avg_price_per_room'] = (df_avg_room_price['price_mean'] / df_avg_room_price['bedrooms']).round(2)
# rename columns
new_columns = ['Neighbourhood', 'Mean Price', 'Median Price', 'Avg # of Bedrooms', 'Avg Price per Bedroom']
df_avg_room_price.columns = new_columns
# sort df by price per room in descending order
df_avg_room_price_sorted = df_avg_room_price.sort_values('Avg Price per Bedroom', ascending=False)

st.dataframe(df_avg_room_price_sorted)

# assign color to each neighborhood
# color palette
color_palette = sns.color_palette("husl", 16)

# create dictionary to assign each neighborhood a color
neighbourhoods = df['neighbourhood_group_cleansed'].unique()
color_mapping = {neighbourhood: mcolors.to_hex(color_palette[i]) for i, neighbourhood in enumerate(neighbourhoods)}

# create new column
df['color'] = df['neighbourhood_group_cleansed'].map(color_mapping)

# display the map
st.map(data=df, color='color')

# NOTE I AM TRYING TO FIGURE OUT HOW TO ADD COLOR KEY TO MAP

