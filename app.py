from sc import Soundcloud

import asyncio, json_config, logging, re
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputFile
logging.basicConfig(level=logging.INFO)

config = json_config.connect('config.json')
sc = Soundcloud()

bot = Bot(token=config['bot_token'])
dp = Dispatcher(bot)

@dp.message_handler(commands=['track', 'playlist'])
async def send_music(message: types.Message):
    command = re.search(r"\/\w*", message.text)
    from_user = message['from']['id']
    if from_user == "2043806344":
        attr_1 = re.split(r"\/\w*", message.text)
        attr_2 = attr_1[1].split()
        href = attr_2[0]
    
        if command.group(0) == "/track":
            await sc.getTrack(href)


        if command.group(0) == "/playlist":
            await sc.getPlaylist(href)
    

# @dp.message_handler()
# async def echo(message: types.Message):
#     await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)