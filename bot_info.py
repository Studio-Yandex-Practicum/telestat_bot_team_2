import os
import sqlite3
import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from settings import Config
from handlers.callback import print_values
from handlers.basic import get_inline


def admins_id():
    con = sqlite3.connect('admins.db')
    with con:
        cur = con.cursor()
        cur.execute("SELECT cast(user_id as INTEGER) as user_id FROM admins")

    users_id = [row[0] for row in cur.fetchall()]
    return users_id


async def start_bot(bot: Bot):
    await bot.send_message(Config.MY_ID, text='Бот запущен.')


async def stop_bot(bot: Bot):
    await bot.send_message(Config.MY_ID, text='Бот остановлен.')


async def start():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=Config.BOT_TOKEN_INFO)

    dp = Dispatcher()
    dp.message.register(get_inline, Command(commands='inline'))
    dp.callback_query.register(print_values)
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
