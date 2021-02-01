import googleapiclient.discovery

import json

import urllib
import urllib.request
from urllib.parse import parse_qs, urlparse

class FetchYoutube:
    def __init__(self, token):
            self.token = token
            
    def parse_playlist(self, url):
        query = parse_qs(urlparse(url).query, keep_blank_values=True)
        playlist_id = query["list"][0]

        print(f'get all playlist items links from {playlist_id}')
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = self.token)

        request = youtube.playlistItems().list(
            part = "snippet",
            playlistId = playlist_id,
            maxResults = 50
        )
        response = request.execute()

        playlist_items = []
        while request is not None:
            response = request.execute()
            playlist_items += response["items"]
            request = youtube.playlistItems().list_next(request, response)

        queue = []
        for t in playlist_items:
            queue.append(f'https://www.youtube.com/watch?v={t["snippet"]["resourceId"]["videoId"]}')

        return queue


    def parse_name(self, url):
        params = {"format": "json", "url": url}
        url = "https://www.youtube.com/oembed"
        query_string = urllib.parse.urlencode(params)
        url = url + "?" + query_string

        with urllib.request.urlopen(url) as response:
            response_text = response.read()
            data = json.loads(response_text.decode())
            return data['title']