import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data #ทำให้ไม่ต้องโหลด data ซ้ำ
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')

#data
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

st.subheader('Map of all pickups')
st.map(data)

hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)


st.subheader('3D map')

import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk


chart_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=["lat", "lon"],
)

st.pydeck_chart(
    pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=40.75,
            longitude=-74,
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data,
                get_position="[lon, lat]",
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                "ScatterplotLayer",
                data=chart_data,
                get_position="[lon, lat]",
                get_color="[200, 30, 0, 160]",
                get_radius=200,
            ),
        ],
    )
)


st.subheader('Rental date')
import datetime
import streamlit as st

d = st.date_input("Rental date input", datetime.date(2019, 7, 6))
st.write("Your Rental date is:", d)

st.subheader('Select box')

import streamlit as st

option = st.selectbox(
    "Apporximate rental hours?",
    ("Less than 1 hour", "1-4 hours", "4-8 hours","more than 8 hours"),
)

st.write("You selected:", option)


if "counter" not in st.session_state:
    st.session_state.counter = 0

st.session_state.counter += 1

st.header(f"Click {st.session_state.counter} times.")
st.button("Click here!!")


st.subheader('Number of pickups by hour (Plotly)')
import plotly.express as px
color = st.color_picker("Pick a bar color", "#00f900")

# Plotly histogram
fig = px.histogram(
    data,
    x=data[DATE_COLUMN].dt.hour,
    nbins=24,
    labels={'x': 'Hour of Day', 'y': 'Number of Pickups'},
    color_discrete_sequence=[color]
)
fig.update_layout(
    bargap=0.2,
    xaxis=dict(tickmode='linear', dtick=1),  # Show all x-axis labels (0 to 23)
    yaxis=dict(range=[0, 800])  # Set max of y-axis to 1000
)
st.plotly_chart(fig)

