from aiogram.utils.helper import Helper, HelperMode, ListItem

class BotStates(Helper):
    mode = HelperMode.snake_case

    SEARCH_STATE = ListItem()
    TRACK_STATE = ListItem()
    PLAYLIST_STATE = ListItem()
    
print(BotStates.all())
