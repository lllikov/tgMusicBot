from aiogram.utils.helper import Helper, HelperMode, ListItem
from future.utils import listitems

class BotStates(Helper):
    mode = HelperMode.snake_case

    SEARCH_STATE = ListItem()
    TRACK_STATE = ListItem()
    PLAYLIST_STATE = ListItem()
    TRACK_DL_STATE = ListItem()
    PLAYLIST_DL_STATE = ListItem()
    DECODE_STATE = ListItem()
    
print(BotStates.all())
# ['decode_state', 'playlist_dl_state', 'playlist_state', 'search_state', 'track_dl_state', 'track_state']