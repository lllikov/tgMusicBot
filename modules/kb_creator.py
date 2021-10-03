from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json


class KeyboardCreator():
    def __init__(self) -> None:
        pass

    def track_create(self, json_array: list):
        k = 1
        buttons = []
        text = ""
        for item in json_array:
            username = item['username']
            title = item['title']
            uri = item['uri']
            text += f"{k}. {username} - {title}\n"
            splitted_uri = uri.split("https://api.soundcloud.com/")
            buttons.append(
                InlineKeyboardButton(k, callback_data=splitted_uri[1])
            )
            k += 1
        return text, buttons


    def playlist_create(self, json_array: list):
        k = 1
        buttons = []
        text = ""
        for item in json_array:
            username = item['username']
            title = item['title']
            uri = item['uri']
            track_count = item['track_count']
            text += f"{k}. {username} - {title}. Количество треков: {track_count}"
            splitted_uri = uri.split("https://api.soundcloud.com/")
            buttons.append(
                InlineKeyboardButton(k, callback_data=splitted_uri[1])
            )
        return text, buttons