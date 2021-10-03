from sc import Soundcloud

import asyncio, json_config, logging, re, os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputFile
logging.basicConfig(level=logging.INFO)

config = json_config.connect('config.json')
sc = Soundcloud()

bot = Bot(token=config['bot_token'])
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_start(message: types.Message):
    return await message.answer(
        """
        👨🏿‍💻 dev. @lllikooov
        🔗 /track [link for him]
        🔗 /playlist [link for him]
        
        """
    )


@dp.message_handler(commands=['track', 'playlist'])
async def send_music(message: types.Message):
    command = re.search(r"\/\w*", message.text)
    from_user = message['from']['id']
    if from_user in config['users']:
        attr_1 = re.split(r"\/\w* ", message.text)
        attr_2 = attr_1[1].split()
        href = attr_2[0]
        
        if command.group(0) == "/track":
            m = await bot.send_message(message.chat.id, "😌 Ищу трек...")
            f = await sc.getTrack(href)
            if f != 0:
                await bot.edit_message_text('🤓 Нашел, сохраняю...', message.chat.id, m.message_id)
                with open(f, 'rb') as fp:
                    await bot.edit_message_text('🥳 Держи!!', message.chat.id, m.message_id)
                    await bot.send_document(message.chat.id, fp)
                    fp.close()
                os.remove(f)
            if f == 0: 
                await bot.edit_message_text('😢 Проблемки с запросом...', message.chat.id, m.message_id)
        
        if command.group(0) == "/playlist":
            m = await bot.send_message(message.chat.id, "😌 Ищу плейлист...")
            fs = await sc.getPlaylist(href)
            if fs != 0:
                await bot.edit_message_text('🤓 Нашел, сохраняю...', message.chat.id, m.message_id)
                for filename in fs:
                    with open(filename, 'rb') as fp:
                        await bot.send_document(message.chat.id, fp)
                        asyncio.sleep(2000)
                        fp.close()
                    os.remove(filename)
                m = await bot.send_message(message.chat.id, "🤯 Это все. Приятного прослушивания")
            if fs == 0:
                await bot.edit_message_text('😢 Проблемки с запросом...', message.chat.id, m.message_id)
    
    if from_user not in config['users']:
        await message.answer('💀 Доступ запрещен.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)