import pandas as pd
import streamlit as st
import plotly.express as px
import data_utils as du


st.title("Streamlit 101: An in-depth introduction")
st.markdown("""Welcome to this in-depth introduction to how to use Streamlit. I'll be analyzing and
            visualizing data AirBnB listing data in Lisbon for 2024.
            
            """)
st.header("Streamlit for newbies")
st.markdown("> I just love to go home, no matter where I am [...]")

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

# use get_data() to get the AirBnB data
df = get_data()

#convert price column to float for analysis later
du.convert_price_to_float(df, 'price')

st.code("""
@st.cache_data
def get_data():
    url = "https://data.insideairbnb.com/portugal/lisbon/lisbon/2024-03-18/data/listings.csv.gz"
    return pd.read_csv(url)
""", language="python")

st.header("Full dataframe limited to 15 entries")
st.dataframe(df.head(15))

# create some columns to filter the dataframe by in an interactive way
standard_columns = ["name", "host_name", "neighbourhood_cleansed", "room_type", "price"]

# create a dataframe view that filters with the standard column names
cols_simple = st.multiselect("Columns", df.columns.tolist(), default=standard_columns)
st.dataframe(df[cols_simple])

st.header("Where are the AirBnB properties in Lisbon?")
# createa  map view of the dataframe
st.map(df)

# find the most expensive properties and their locations
st.header("Where are the most expensive properties located?")
st.subheader("On a map")
st.markdown("The following map shows the top 1% most expensive Airbnbs priced at $800 and above in Lisbon.")
st.map(df.query("price>=800")[["latitude", "longitude"]].dropna(how="any"))
st.subheader("In a table")
st.markdown("Following are the top five most expensive properties.")
st.write(df[standard_columns].query("price>=800").sort_values("price", ascending=False).head())


# find the average and median price per type of room/lodging
st.header("What's the average price per night and median price per night for each type of rental?")
# Calculate mean and round
mean_prices = df.groupby("room_type")['price'].mean().reset_index().round(2)
# Calculate median and round
median_prices = df.groupby("room_type")['price'].median().reset_index().round(2)
# Merge the results on 'room_type'
result = pd.merge(mean_prices, median_prices, on="room_type", suffixes=('_mean', '_median'))
# Format the prices and display
result = result.sort_values("price_mean", ascending=False)
result['price_mean'] = result['price_mean'].apply(lambda x: f"${x:.2f}")
result['price_median'] = result['price_median'].apply(lambda x: f"${x:.2f}")
result = result.rename(columns={'room_type':'Room Type',
                                'price_mean':'Average Price', 'price_median':'Median Price'})
st.table(result)

# find the hosts with the most properties listed in Lisbon
st.header("Which host has the most properties listed?")
listingcounts = df.host_id.value_counts()
top_host_1 = df.query('host_id==@listingcounts.index[0]')
top_host_2 = df.query('host_id==@listingcounts.index[1]')
st.write(f"""**{top_host_1.iloc[0].host_name}** is at the top with {listingcounts.iloc[0]} property listings.
**{top_host_2.iloc[1].host_name}** is second with {listingcounts.iloc[1]} listings. Following are randomly chosen
listings from the two displayed as JSON using [`st.json`](https://streamlit.io/docs/api.html#streamlit.json).""")

# find the distribution in property price for a certain price range
st.header("What is the distribution of property price?")
st.write("""Select a custom price range from the side bar to update the histogram below displayed as a Plotly chart using
[`st.plotly_chart`](https://streamlit.io/docs/api.html#streamlit.plotly_chart).""")
values = st.sidebar.slider("Price range", float(df.price.min()), float(df.price.clip(upper=1000.).max()), (50., 300.))
f = px.histogram(df.query(f"price.between{values}"), x="price", nbins=15, title="Price distribution")
f.update_xaxes(title="Price")
f.update_yaxes(title="No. of listings")
st.plotly_chart(f)