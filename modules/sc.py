import json_config
from sclib.asyncio import SoundcloudAPI, Track, Playlist

config = json_config.connect('./config/config.json')

class Soundcloud: 
    def __init__(self):
        self.api = SoundcloudAPI(config['sc_client_id'])


    async def getTrack(self, t_link: str):
        try:
            print(f'_. downloading track starting now.')
            track = await self.api.resolve(t_link)
            assert type(track) is Track
            filename = f'{track.artist} - {track.title}.mp3'
            print(f'-. {filename} downloaded! saving to file.')
            with open(filename, "wb+") as fp:
                await track.write_mp3_to(fp)
            return filename
        except:
            print('error')
            return 0

    async def getPlaylist(self, p_link: str):
        try:
            print(f'-. downloading playlist starting now.')
            playlist = await self.api.resolve(p_link)
            filenames = []
            assert type(playlist) is Playlist
            for track in playlist.tracks:
                filename = f'{track.artist} - {track.title}.mp3'
                filenames.append(filename)
                print(f'_. {filename} downloaded! saving to file.')
                with open(filename, "wb+") as fp:
                    await track.write_mp3_to(fp)
            return filenames
        except: 
            print('error')
            return 0