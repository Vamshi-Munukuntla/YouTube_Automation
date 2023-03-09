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
            part='snippet,statistics',
            id=','.join(video_ids[i:i + 50]))
        response = request.execute()
        for video in response['items']:
            video_stats = dict(Title=video['snippet'].get('title', None),
                               Published_date=video['snippet'].get('publishedAt', None),
                               Views=video['statistics'].get('viewCount', None),
                               Likes=video['statistics'].get('likeCount', None),
                               Favorite=video['statistics'].get('favoriteCount', None),
                               Comments=video['statistics'].get('commentCount', None)
                               )

            all_video_stats.append(video_stats)

    return all_video_stats
