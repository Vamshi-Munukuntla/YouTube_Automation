import streamlit as st
from googleapiclient.discovery import build
import pandas as pd
from get_data import get_channel_stats, get_video_ids, get_video_details

st.title('YouTube Data Automation')
st.subheader('by Vamshi Munukuntla')

SOCIAL_MEDIA = {
    "GitHub": "https://github.com/Vamshi-Munukuntla",
    "LinkedIn": "https://www.linkedin.com/in/vamshi-kumar87/"
}


st.write('#')
cols = st.columns(len(SOCIAL_MEDIA))
for index, (platform, link) in enumerate(SOCIAL_MEDIA.items()):
    cols[index].write(f"[{platform}]({link})")


youtube_api = st.text_input(label='Please enter the youtube api key: ')
channel_id = st.text_input(label='Please enter the youtube channel id')

if (youtube_api != "") & (channel_id != ""):
    youtube = build('youtube', 'v3', developerKey=youtube_api)

    channel_statistics = get_channel_stats(youtube, channel_id)
    channel_data = pd.DataFrame(channel_statistics)
    Channel_name = channel_statistics[0]['Channel_name']
    st.success(f"Fetching data from {Channel_name.upper()}'s channel.")

    playlist_ids = channel_data['playlist_id'][0]
    st.markdown('This takes a while, please be patient.')

    video_ids = get_video_ids(youtube, playlist_ids)
    video_details = get_video_details(youtube, video_ids)

    st.caption('Top 5 Recently uploaded Videos')
    final_df = pd.DataFrame(video_details)
    st.dataframe(final_df.head())

    # Save the dataframe into a csv file
    @st.cache_data
    def convert_df(data):
        return data.to_csv(index=False)


    csv_file = convert_df(final_df)

    # Download the data
    st.download_button(
        label="Download Complete data as CSV file",
        data=csv_file,
        file_name='youtube_data.csv',
        mime='text/csv',
    )

# api_key = "AIzaSyBZM6dAN2JOqAQ9g6ZbO2SatXmB0wUwxGM"
# channel_ids = "UCNU_lfiiWBdtULKOw6X0Dig"
