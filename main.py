import streamlit as st
from googleapiclient.discovery import build
import pandas as pd
from get_data import get_channel_stats, get_video_ids, get_video_details, convert_YouTube_duration_to_seconds

st.title('YouTube Data Automation')
st.write('Get your favorite youtube channel data in matter of seconds.')
st.subheader('Created by Vamshi Munukuntla')

SOCIAL_MEDIA = {
    "GitHub": "https://github.com/Vamshi-Munukuntla",
    "LinkedIn": "https://www.linkedin.com/in/vamshi-kumar87/"
}


st.write('Follow me on:')
cols = st.columns(len(SOCIAL_MEDIA)+2)
for index, (platform, link) in enumerate(SOCIAL_MEDIA.items()):
    cols[index].write(f"[{platform}]({link})")


st.write('-'*100)
youtube_api = st.text_input(label='Please enter the YOUTUBE API KEY: ')
st.caption("Eg: AIzaSyBZMdAN2JOSqAQ96ZbO2SBatXmB0wUwxGM(it's a dummy api, only for reference)")
if youtube_api == "AIzaSyBZMdAN2JOSqAQ96ZbO2SBatXmB0wUwxGM":
    st.write("It's a dummy api key, provided for reference")
    # st.write('you can get your own api key for free for here: {}')

st.write('#')
channel_id = st.text_input(label='Please enter the YOUTUBE CHANNEL ID')
if st.button('Few Channel ids you can try: '):
    ids = pd.read_csv('channel_ids.csv')
    st.table(ids)

st.write("#")
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
    final_df['Video_Duration_in_seconds'] = final_df['Video_Duration'].apply(convert_YouTube_duration_to_seconds)
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

