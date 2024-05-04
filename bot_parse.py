from pyrogram import Client, filters
from settings import Config
from pyrogram.types import Message
from permissions.permissions import check_authorization, create_admin


bot_parse = Client(
    "my_account", api_id=Config.API_ID,
    api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN
)


@bot_parse.on_message(filters.command('start'))
async def command_start(
    client: Client,
    message: Message
):
    """Обработчик команды на запуск бота по сбору данных."""

    if not await check_authorization(message.from_user.id):
        await client.send_message(
            message.chat.id,
            'Управлять ботом могут только Администраторы.'
        )
    else:
        await client.send_message(
            message.chat.id,
            'Вы прошли авторизацию!',
        )

        @bot_parse.on_message(filters.command('new_admin'))
        async def new_admin(
            client: Client,
            message: Message
        ):
            await client.send_message(
                message.chat.id,
                'Введите user_id и username администратора через запятую'
            )

            @bot_parse.on_message(filters.text)
            async def get_user(
                client: Client,
                message: Message
            ):
                user = message.text.split(', ')
                data = {
                    'user_id': int(user[0]),
                    'username': user[1],
                    'is_admin': True
                }
                if not await create_admin(data):
                    await client.send_message(
                        message.chat.id,
                        'Ошибка'
                    )
                else:
                    await client.send_message(
                        message.chat.id,
                        'Новый админ создан'
                    )