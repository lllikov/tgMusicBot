from sc import Soundcloud
import json, json_config, asyncio, requests
from urllib.parse import quote

sc = Soundcloud()
config = json_config.connect('config.json')

class SoundcloudSearcher:
    def __init__(self) -> None:
        pass

    def request_tracks(self, track_name, offset=0):
        limit = 20
        track_name_quotes = quote(track_name)
        href_track = f'https://api-v2.soundcloud.com/search?q={track_name_quotes}&variant_ids=2382%2C2375&facet=model&client_id={config["sc_client_id"]}&limit={limit}&offset={offset}&linked_partitioning=1&app_version=1633082668&app_locale=en'
        r = requests.get(href_track)
        responses = json.loads(r.text)
        info = []
        for response in responses['collection']:
            if response['kind'] == 'track':
                uri = response['uri']
                title = response['title']
                username = response['user']['username']
                info.append(
                    {
                        "username": username,
                        "title": title, 
                        "uri": uri
                    }
                )
        info_json = json.dumps(info, indent=4, ensure_ascii=False)
        return info_json
    
    def request_playlists(self, playlist_name, offset=0):
        limit = 20
        playlist_name_quotes = quote(playlist_name)
        href_playlist = f'https://api-v2.soundcloud.com/search/playlists_without_albums?q={playlist_name_quotes}&client_id={config["sc_client_id"]}&limit={limit}&offset={offset}app_version=1633082668&app_locale=en'
        r = requests.get(href_playlist)
        responses = json.loads(r.text)
        info = []
        for response in responses['collection']:
            uri = response['uri']
            title = response['title']
            username = response['user']['username']
            track_count = response['track_count']
            info.append(
                {
                    "username": username,
                    "title": title,
                    "track_count": track_count,
                    "uri": uri
                }
            )
        info_json = json.dumps(info, indent=4, ensure_ascii=False)
        return info_json