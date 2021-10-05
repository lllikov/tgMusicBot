import json
from urllib import parse

from aiogram.types.message import ParseMode
from modules.sc import Soundcloud
from modules.soundcloud_searcher import SoundcloudSearcher
from modules.utils import *
from modules.kb_creator import KeyboardCreator
import modules.url_decoder as url_decode
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


# bot states
# ['decode_state', 'playlist_dl_state', 'playlist_state', 'search_state', 'track_dl_state', 'track_state']

deS = 0
pDlS = 1
pS = 2
ss = 3
tDlS = 4
tS = 5


playlist_button = InlineKeyboardButton(mes['pBut'], callback_data="playlist_button")
track_button = InlineKeyboardButton(mes['tBut'], callback_data="track_button")
select_search = InlineKeyboardMarkup(row = 2).add(playlist_button, track_button)

@dp.message_handler(commands=['search', 's', 'поиск', 'п'])
async def searching(message: types.Message):
    if message.from_user.id in config['users']:
        return await message.answer(mes['search_1'], reply_markup=select_search)
    else: return await message.answer(mes['not_user'])


@dp.message_handler(commands=['start'])
async def send_start(message: types.Message):
    if message.from_user.id in config['users']:
        state = dp.current_state(user = message.from_user.id)
        await state.reset_state()
        return await message.answer(mes['start'], reply_markup=kb.start_keyboard())
    else: return await message.answer(mes['not_user'])


@dp.message_handler(commands=['track', 't', 'т'])
async def set_state_track_dl(message: types.Message):
    state = dp.current_state(user = message.from_user.id)
    await message.answer(mes['track_dl'])
    return await state.set_state(BotStates.all()[tDlS])


@dp.message_handler(commands=['playlist', 'p', 'п'])
async def set_state_playlist_dl(message: types.Message):
    state = dp.current_state(user = message.from_user.id)
    await message.answer(mes['playlist_dl'])
    return await state.set_state(BotStates.all()[pDlS])


@dp.message_handler(commands=['urldecode', 'url', 'u'])
async def decode_start(message: types.Message):
    state = dp.current_state()
    await message.answer(mes['decode_start'])
    return await state.set_state(BotStates.all()[deS])


@dp.callback_query_handler(lambda c: c.data == 'track_button')
async def track_searching(callback_query: types.CallbackQuery):
    from_user = callback_query['from']['id']
    chat_id = callback_query['message']['chat']['id']
    state = dp.current_state(user = from_user)
    await state.set_state(BotStates.all()[tS])
    await bot.send_message(chat_id, mes['search_track'])
    return await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data == 'playlist_button')
async def playlist_searching(callback_query: types.CallbackQuery):
    from_user = callback_query['from']['id']
    chat_id = callback_query['message']['chat']['id']
    state = dp.current_state(user = from_user)
    await state.set_state(BotStates.all()[pS])
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


@dp.message_handler(state = BotStates.TRACK_DL_STATE)
async def track_dl(message: types.Message):
    state = dp.current_state()
    href = message.text
    m = await message.answer(mes['request_message'])
    track = await sc.getTrack(href)
    if track != 0 and track != 1:
        with open(track, "rb") as f:
            await bot.send_document(message.chat.id, f)
            f.close()
        os.remove(track)
        await bot.delete_message(message.chat.id, m.message_id)
        return await state.reset_state()
    if track == 0:
        await message.answer(mes['error'])
        return await state.reset_state()
    if track == 1:
        await message.answer(mes['error_writing'])
        return await state.reset_state()
    

@dp.message_handler(state = BotStates.PLAYLIST_DL_STATE)
async def playlist_dl(message: types.Message):
    state = dp.current_state()
    href = message.text
    m = await message.answer(mes['request_message'])
    playlist = await sc.getPlaylist(href)
    if playlist != 0:
        for track in playlist:
            with open(track, "rb") as f:
                await bot.send_document(message.chat.id, f)
                f.close()
            os.remove(track)
        await bot.delete_message(message.chat.id, m.message_id)
        await message.answer(mes['playlist_end'])
        return await state.reset_state()
    if playlist == 0:
        await message.answer(mes['error'])
        return await state.reset_state()

@dp.message_handler(state = BotStates.DECODE_STATE)
async def decode(message: types.Message):
    state = dp.current_state()
    link_to_decode = message.text
    link_decoded = url_decode.url_decode(link_to_decode)
    if link_decoded != 0:
        await message.answer(mes['decode_finish'])
        await message.answer(link_decoded, disable_web_page_preview=True)
    if link_decoded == 0:
        await message.answer(mes['decode_error'])
    return await state.reset_state()


@dp.callback_query_handler(lambda c: "/" in c.data)
async def search_handler(callback_query: types.CallbackQuery):
    raw_data = callback_query.data
    processed_data = raw_data.split("/")
    print(processed_data)
    href = "https://api.soundcloud.com"
    if processed_data[0] == "playlists":
        f = await sc.getPlaylist(f'{href}/playlists/{processed_data[1]}')
        if f != 0:
            for path in f:
                with open(path, "rb") as fp:
                    await bot.send_document(callback_query.from_user.id, fp)
                    fp.close()
                    await asyncio.sleep(2)
                os.remove(path)
        if f == 0:
            await bot.send_message(callback_query.from_user.id, mes['error'])    
        return await callback_query.answer()
    if processed_data[0] == "tracks":
        f = await sc.getTrack(f'{href}/tracks/{processed_data[1]}')
        if f != 0:
            with open(f, "rb") as fp:
                await bot.send_document(callback_query.from_user.id, fp)
                fp.close()
            os.remove(f)
        if f == 0:
            await bot.send_message(callback_query.from_user.id, mes['error'])    
        return await callback_query.answer(text="")






# @dp.message_handler(commands=['track', 'playlist'])
# async def send_music(message: types.Message):
#     command = re.search(r"\/\w*", message.text)
#     from_user = message['from']['id']
#     if from_user in config['users']:
#         attr_1 = re.split(r"\/\w* ", message.text)
#         attr_2 = attr_1[1].split()
#         href = attr_2[0]
        
#         if command.group(0) == "/track":
#             m = await bot.send_message(message.chat.id, mes['searching_track'])
#             f = await sc.getTrack(href)
#             if f != 0:
#                 await bot.edit_message_text(mes['saving_track'], message.chat.id, m.message_id)
#                 with open(f, 'rb') as fp:
#                     await bot.edit_message_text(mes['sending_track'], message.chat.id, m.message_id)
#                     await bot.send_document(message.chat.id, fp)
#                     fp.close()
#                 os.remove(f)
#             if f == 0: 
#                 await bot.edit_message_text(mes['error'], message.chat.id, m.message_id)
        
#         if command.group(0) == "/playlist":
#             m = await bot.send_message(message.chat.id, mes['searcging_playlist'])
#             fs = await sc.getPlaylist(href)
#             if fs != 0:
#                 await bot.edit_message_text(mes['saving'], message.chat.id, m.message_id)
#                 for filename in fs:
#                     with open(filename, 'rb') as fp:
#                         await bot.send_document(message.chat.id, fp)
#                         asyncio.sleep(2000)
#                         fp.close()
#                     os.remove(filename)
#                 m = await bot.send_message(message.chat.id, mes['after_playlist'])
#             if fs == 0:
#                 await bot.edit_message_text(mes['error'], message.chat.id, m.message_id)
    
#     if from_user not in config['users']:
#         await message.answer(mes['not_user'])



@dp.message_handler()
async def button_handler(message: types.Message):
    if message.text == mes["a_button"]:
        await bot.delete_message(message.chat.id, message.message_id)
        return await searching(message)
    if message.text == mes["b_button"]:
        await bot.delete_message(message.chat.id, message.message_id)
        return await set_state_track_dl(message)
    if message.text == mes["c_button"]:
        await bot.delete_message(message.chat.id, message.message_id)
        return await set_state_playlist_dl(message)
    if message.text == mes["d_button"]:
        await bot.delete_message(message.chat.id, message.message_id)
        return await decode_start(message)



async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_shutdown=shutdown)