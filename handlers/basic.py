from aiogram import Bot
from aiogram.types import Message
from keyboard.inline import get_inline_keyboard


async def get_inline(message: Message, bot: Bot):
    await message.answer(f'Hi {message.from_user.first_name} inline',
                         reply_markup=get_inline_keyboard())