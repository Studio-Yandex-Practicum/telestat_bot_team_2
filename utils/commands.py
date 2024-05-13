from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commads = [
        BotCommand(
            command='start',
            description='Начать'
        ),
        BotCommand(
            command='inline',
            description='Показать клавиатуру inline'
        )
    ]
    await bot.set_my_commands(commads, BotCommandScopeDefault())