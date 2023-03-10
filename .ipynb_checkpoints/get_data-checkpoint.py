# Function to get channel statistics
def get_channel_stats(youtube, channel_ids):
    all_data = []

    request = youtube.channels().list(
        part='snippet, contentDetails, statistics',
        id=channel_ids)
    response = request.execute()
    for i in range(len(response['items'])):
        data = dict(Channel_name=response['items'][i]['snippet']['title'],
                    Subscribers=response['items'][i]['statistics']['subscriberCount'],
                    Total_Videos=response['items'][i]['statistics']['videoCount'],
                    Total_Views=response['items'][i]['statistics']['viewCount'],
                    playlist_id=response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
        all_data.append(data)

    return all_data


# Function to get video ids
def get_video_ids(youtube, playlist_id):
    request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId=playlist_id,
        maxResults=50)
    response = request.execute()

    video_ids = []

    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])

    next_page_token = response.get('nextPageToken')
    more_pages = True
    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            request = youtube.playlistItems().list(
                part='contentDetails',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token)
            response = request.execute()

        for i in range(len(response['items'])):
            video_ids.append(response['items'][i]['contentDetails']['videoId'])

        next_page_token = response.get('nextPageToken')

    return video_ids


# Function to get video details
def get_video_details(youtube, video_ids):
    all_video_stats = []

    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part='snippet,statistics, contentDetails, topicDetails',
            id=','.join(video_ids[i:i + 50]))
        response = request.execute()
        for video in response['items']:
            video_stats = dict(unique_video_id=video.get('id', None),
                               Title=video['snippet'].get('title', None),
                               Video_Description=video['snippet'].get("description", None),
                               Tags=video['snippet'].get("tags", None),
                               Published_date=video['snippet']['publishedAt'].split('T')[0],
                               Published_time=video['snippet']['publishedAt'].split('T')[1][:-1],
                               Video_Duration=video['contentDetails']['duration'],
                               Views=video['statistics'].get('viewCount', None),
                               Likes=video['statistics'].get('likeCount', None),
                               Favorite=video['statistics'].get('favoriteCount', None),
                               Comments=video['statistics'].get('commentCount', None),
                               )

            all_video_stats.append(video_stats)

    return all_video_stats


def convert_YouTube_duration_to_seconds(duration):
    day_time = duration.split('T')
    day_duration = day_time[0].replace('P', '')
    day_list = day_duration.split('D')
    if len(day_list) == 2:
        day = int(day_list[0]) * 60 * 60 * 24
        day_list = day_list[1]
    else:
        day = 0
        day_list = day_list[0]
        hour_list = day_time[1].split('H')
    if len(hour_list) == 2:
        hour = int(hour_list[0]) * 60 * 60
        hour_list = hour_list[1]
    else:
        hour = 0
        hour_list = hour_list[0]
    minute_list = hour_list.split('M')
    if len(minute_list) == 2:
        minute = int(minute_list[0]) * 60
        minute_list = minute_list[1]
    else:
        minute = 0
        minute_list = minute_list[0]
    second_list = minute_list.split('S')
    if len(second_list) == 2:
        second = int(second_list[0])
    else:
        second = 0
    return day + hour + minute + second
