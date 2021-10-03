import json
from urllib import parse

from aiogram.types.message import ParseMode
from modules.sc import Soundcloud
from modules.soundcloud_searcher import SoundcloudSearcher
from modules.utils import *
from modules.kb_creator import KeyboardCreator
import asyncio, json_config, logging, re, os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
logging.basicConfig(level=logging.INFO)


config = json_config.connect('config/config.json')
mes = json_config.connect('config/messages.json')
sc = Soundcloud()
sc_searcher = SoundcloudSearcher()
kb = KeyboardCreator()

bot = Bot(token=config['bot_token'])
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


playlist_button = InlineKeyboardButton(mes['pBut'], callback_data="playlist_button")
track_button = InlineKeyboardButton(mes['tBut'], callback_data="track_button")
select_search = InlineKeyboardMarkup(row = 2).add(playlist_button, track_button)

@dp.message_handler(commands=['search', 's', 'поиск', 'п'])
async def searching(message: types.Message):
    return await message.answer(mes['search_1'], reply_markup=select_search)

@dp.callback_query_handler(lambda c: c.data == 'track_button')
async def track_searching(callback_query: types.CallbackQuery):
    from_user = callback_query['from']['id']
    chat_id = callback_query['message']['chat']['id']
    state = dp.current_state(user = from_user)
    await state.set_state(BotStates.all()[2])
    await bot.send_message(chat_id, mes['search_track'])
    return await callback_query.answer()

@dp.callback_query_handler(lambda c: c.data == 'playlist_button')
async def playlist_searching(callback_query: types.CallbackQuery):
    from_user = callback_query['from']['id']
    chat_id = callback_query['message']['chat']['id']
    state = dp.current_state(user = from_user)
    await state.set_state(BotStates.all()[0])
    await bot.send_message(chat_id, mes['search_playlist'])
    return await callback_query.answer()

@dp.message_handler(state=BotStates.TRACK_STATE)
async def track_search(message: types.Message):
    state = dp.current_state(user = message.from_user.id)
    req = message.text
    res = sc_searcher.request_tracks(req)
    json_res = json.loads(res)
    kb_creator = kb.track_create(json_res)
    await message.answer(kb_creator[0], reply_markup=kb_creator[1])
    return await state.reset_state()


@dp.message_handler(state=BotStates.PLAYLIST_STATE)
async def playlist_search(message: types.Message):
    state = dp.current_state(user = message.from_user.id)
    req = message.text
    res = sc_searcher.request_playlists(req)
    json_res = json.loads(res)
    kb_creator = kb.playlist_create(json_res)
    await message.answer(kb_creator[0], reply_markup=kb_creator[1])
    return await state.reset_state()

@dp.message_handler(commands=['start'])
async def send_start(message: types.Message):
    return await message.answer(mes['start'])


@dp.message_handler(commands=['track', 'playlist'])
async def send_music(message: types.Message):
    command = re.search(r"\/\w*", message.text)
    from_user = message['from']['id']
    if from_user in config['users']:
        attr_1 = re.split(r"\/\w* ", message.text)
        attr_2 = attr_1[1].split()
        href = attr_2[0]
        
        if command.group(0) == "/track":
            m = await bot.send_message(message.chat.id, mes['searching_track'])
            f = await sc.getTrack(href)
            if f != 0:
                await bot.edit_message_text(mes['saving_track'], message.chat.id, m.message_id)
                with open(f, 'rb') as fp:
                    await bot.edit_message_text(mes['sending_track'], message.chat.id, m.message_id)
                    await bot.send_document(message.chat.id, fp)
                    fp.close()
                os.remove(f)
            if f == 0: 
                await bot.edit_message_text(mes['error'], message.chat.id, m.message_id)
        
        if command.group(0) == "/playlist":
            m = await bot.send_message(message.chat.id, mes['searcging_playlist'])
            fs = await sc.getPlaylist(href)
            if fs != 0:
                await bot.edit_message_text(mes['saving'], message.chat.id, m.message_id)
                for filename in fs:
                    with open(filename, 'rb') as fp:
                        await bot.send_document(message.chat.id, fp)
                        asyncio.sleep(2000)
                        fp.close()
                    os.remove(filename)
                m = await bot.send_message(message.chat.id, mes['after_playlist'])
            if fs == 0:
                await bot.edit_message_text(mes['error'], message.chat.id, m.message_id)
    
    if from_user not in config['users']:
        await message.answer(mes['not_user'])


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_shutdown=shutdown)