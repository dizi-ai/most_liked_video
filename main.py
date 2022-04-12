import sys
import os
from googleapiclient.discovery import build


def most_liked_videos(api_key, playlist_id):
    service = build('youtube', 'v3', developerKey=api_key)
    nextPageToken = None
    videos_by_likes = []
    try:
        while True:
            videos = []
            playlist_req = service.playlistItems().list(
                part= 'contentDetails',
                playlistId= playlist_id,
                pageToken = nextPageToken,
                maxResults = 25
                )
            
            playlist_res = playlist_req.execute()
            
            for video in playlist_res['items']:
                videos.append(video['contentDetails']['videoId'])
                
            videos_req = service.videos().list(part='statistics', id=','.join(videos))
            videos_res = videos_req.execute()
            
            for vid in videos_res['items']:
                video_id = vid['id']
                video_stats = vid['statistics']
                videos_by_likes.append({'url':f'https://youtu.be/{video_id}',
                                        'likes': int(video_stats['likeCount'])})
                
            nextPageToken = playlist_res.get('nextPageToken')
            if not nextPageToken:
                break
    except:
        print('Invalid API key or playlist id')
        
    videos_by_likes.sort(key= lambda vid: vid['likes'], reverse=True)
    return videos_by_likes


if __name__ == '__main__':
    api_key = ''
    playlist = ''
    if len(sys.argv) < 3:
        print('pass the parameters:')
        print('python3 main.py #YOUR_API_KEY #PLAYLIST_ID')
        print('OR')
        print('python3 main.py -f #FILE_WITH_YOUR_API_KEY #PLAYLIST_ID')
        exit()
    elif sys.argv[1] == '-f':
        filename = sys.argv[2]
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                api_key=f.read()
        else:
            print("File doesn't exist")
            exit()
        playlist = sys.argv[3]
    else:
        api_key = sys.argv[1]
        print(f'filename: {api_key}')
        playlist = sys.argv[2]
        print(f'playlist: {playlist}')
    
    vbl = most_liked_videos(api_key=api_key, playlist_id=playlist)
    for video in vbl:
        print(video)