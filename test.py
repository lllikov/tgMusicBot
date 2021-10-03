# import json


# links= []
# i = 0
# while i < 10:
#     username = f'dora{i}' 
#     title = f'mladhaya sestra{i}'
#     uri = f'https://soundcloud/track/dfgdsfg{i}'
    
#     links.append(
#         {
#             "username": username,
#             "title": title,
#             "uri": uri
#         }
#     )

#     i += 1

# print(json.dumps(links, indent=4))

# import asyncio, json_config, logging, re, os
# config = json_config.connect('config.json')
# print(config['users'])

# import json
# from soundcloud_searcher import SoundcloudSearcher

# sc = SoundcloudSearcher()

# a = json.loads(sc.request_tracks('дора'))
# for item in a:
#     print(item)


# a = "https://api.soundcloud.com/playlists/1289447848"
# splitted = a.split("https://api.soundcloud.com/")
# print(splitted[1])

# from modules.soundcloud_searcher import SoundcloudSearcher

# sc = SoundcloudSearcher()
# a = sc.request_tracks("дора")
# print(a)




# import json
# from modules.kb_creator import KeyboardCreator
# from modules.soundcloud_searcher import SoundcloudSearcher
# sc_s = SoundcloudSearcher()
# res=  sc_s.request_tracks(track_name ='дора')

# kb = KeyboardCreator()
# a = kb.track_create(json.loads(res))

# print(a[1])

import asyncio
from modules.sc import Soundcloud

sc = Soundcloud()

if __name__ == "__main__":
    asyncio.run(sc.getPlaylist("https://api.soundcloud.com/playlists/1325745214"))