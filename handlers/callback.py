from aiogram import Bot
from aiogram.types import CallbackQuery
from handlers.sheets import get_values


async def print_values(call: CallbackQuery, bot: Bot):
    answer = get_values()
    await call.message.answer(f'Количество участников группы: {answer}')
    await call.answer()
