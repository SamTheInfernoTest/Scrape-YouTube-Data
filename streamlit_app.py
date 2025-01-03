import altair as alt
import pandas as pd
import streamlit as st

from youtubeScraper import getData


# Show the page title and description.
st.set_page_config(page_title="Movies dataset", page_icon="📺")
st.title("📺 YouTube Data Scraper")
st.header("By Suman Saurabh")

st.write(
    """
    YouTube Data Scrapper fetches and analyzes YouTube data using the YouTube Data API. It automates the extraction of video details, channel stats, and etc, providing insights into content performance and audience engagement.
    """
)



col1, col2 = st.columns(2)

with col1:
    genre = st.text_input("Enter the genre:", "Music")
    number = st.number_input("Number of videos:", min_value=1, max_value=500, value=10, step=1)

with col2:
    _ = st.write("")
    _ = st.write("")
    get_data = st.button("Get Data", type="primary",  use_container_width=True)



if get_data:
    with st.container():
        st.subheader("This is gathered Data")
        with st.spinner("## This will Take A While..."):
            df = getData(genre, number)
        st.dataframe(df, use_container_width=True)

