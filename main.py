import streamlit as st
from googleapiclient.discovery import build
import pandas as pd
from get_data import get_channel_stats, get_video_ids, get_video_details


youtube_api = st.text_input(label='Please enter the api key')
channel_id = st.text_input(label='Please enter the channel id')

# api_key = "AIzaSyBZM6dAN2JOqAQ9g6ZbO2SatXmB0wUwxGM"
# channel_ids = "UCNU_lfiiWBdtULKOw6X0Dig"


api_key = youtube_api
channel_ids = channel_id

youtube = build('youtube', 'v3', developerKey=api_key)

channel_statistics = get_channel_stats(youtube, channel_ids)
df = pd.DataFrame(channel_statistics)
st.dataframe(df)


playlist_ids = df['playlist_id'][0]
video_ids = get_video_ids(youtube, playlist_ids)

video_details = get_video_details(youtube, video_ids)
final_df = pd.DataFrame(video_details)
st.dataframe(final_df)


# Save the dataframe into a csv file
@st.cache_data
def convert_df(data):
    return data.to_csv(index=False)


csv_file = convert_df(final_df)

# Download the data
st.download_button(
    label="Download data as CSV",
    data=csv_file,
    file_name='youtube_data.csv',
    mime='text/csv',
)

