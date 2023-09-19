import os
from time import sleep

from aiogram import Bot, Dispatcher, executor, types

from etc import help as helpmessage
from etc import command_parse


token = ''
chatID = 
myname = os.getlogin()

def start():
    global loged
    loged = False

    bot = Bot(token=token)
    dp = Dispatcher(bot)

    @dp.message_handler(commands=['name'])
    async def say_my_name(message: types.Message):
        if message.chat.id == chatID:
            await bot.send_message(message.chat.id, f'{myname} is online.')

    @dp.message_handler(commands=[myname])
    async def login(message: types.Message):
        global loged
        if message.chat.id == chatID:
            if loged:
                loged = False
                await bot.send_message(message.chat.id, f'{myname} unlogged.')
            else:
                loged = True
                await bot.send_message(message.chat.id, f'{myname} logged.')
    
    @dp.message_handler(commands=['help'])
    async def help(message: types.Message):
        global loged
        if message.chat.id == chatID and loged:
            await bot.send_message(message.chat.id, helpmessage)
    
    @dp.message_handler(content_types=['text'])
    async def parse_command(message: types.Message):
        global loged
        if message.chat.id == chatID and loged and '/' in message.text:
            command_parse(message.text, chatID, token)

    @dp.message_handler(content_types=['any'])
    async def unknown_message(message: types.Message):
        if message.chat.id == chatID and loged:
            if document := message.document:
                await document.download(destination_file=f'{document.file_name}')

    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    while True:
        try:
            start()
        except BaseException:
            sleep(1)