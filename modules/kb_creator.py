from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json


class KeyboardCreator():
    def __init__(self) -> None:
        pass

    def track_create(self, json_array: list):
        k = 1

        keyboard = InlineKeyboardMarkup(row_width=5)
        next_button = InlineKeyboardButton("next", callback_data='next_page')
        keyboard.add(next_button)
        text = ""
        for item in json_array:
            username = item['username']
            title = item['title']
            uri = item['uri']
            text += f"{k}. {username} - {title}\n"
            splitted_uri = uri.split("https://api.soundcloud.com/")
            but = InlineKeyboardButton(k, callback_data = splitted_uri[1])
            keyboard.insert(but)
            k += 1
        # keyboard = json.dumps([ob.__dict__ for ob in buttons])
        # keyboard.add()
        

            

        return text, keyboard


    def playlist_create(self, json_array: list):
        k = 1
        text = ""
        keyboard = InlineKeyboardMarkup(row_width=5)
        next_button = InlineKeyboardButton("next", callback_data='next_page')
        keyboard.add(next_button)
        for item in json_array:
            username = item['username']
            title = item['title']
            uri = item['uri']
            track_count = item['track_count']
            text += f"{k}. {username} - {title}.    Количество треков: {track_count}\n"
            splitted_uri = uri.split("https://api.soundcloud.com/")
            but = InlineKeyboardButton(k, callback_data = splitted_uri[1])
            keyboard.insert(but)
            k += 1
        return text, keyboard