import os
from pyrogram import Client, filters
from settings import Config
from aiogoogle import Aiogoogle
from pyrogram.types import Message
from constants import Commands

from buttons.buttons import (
    admin_keyboard,
    data_collection_keyboard,
    main_menu_keyboard
)
from permissions.permissions import (
    check_admin, check_superuser
)
from core.admin import create_admin, delete_admin, get_all_admins
from core.validation import validate_data_on_create, validate_data_on_delete
from services.get_data_tlg import GetParticipantInfo
from services.google_api_service import (
    check_spreadsheet_exist,
    create_sheet,
    create_spreadsheet,
    spreadsheet_update_values
)

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

    if not await check_admin(message.from_user.id):
        await client.send_message(
            message.chat.id,
            'Управлять ботом могут только Администраторы.'
        )
    else:
        await client.send_message(
            message.chat.id,
            'Вы прошли авторизацию!',
            reply_markup=main_menu_keyboard
        )


@bot_parse.on_message(filters.regex(Commands.back.value))
async def main_menu(
    client: Client,
    message: Message
):
    """Меню с основными разделами бота."""

    await client.send_message(
        message.chat.id,
        'Выберите раздел',
        reply_markup=main_menu_keyboard
    )


@bot_parse.on_message(filters.regex(Commands.admin_management.value))
async def admin_buttons(
    client: Client,
    message: Message
):
    """Действия, связанные с админами."""

    await client.send_message(
        message.chat.id,
        text='Выберите действие',
        reply_markup=admin_keyboard
    )

    @bot_parse.on_message(filters.regex(Commands.add_admin.value))
    async def new_admin(
        client: Client,
        message: Message
    ):
        if not await check_superuser(message.from_user.id):
            await client.send_message(
                message.chat.id, 'Добавить админа может только суперпользователь!')
        else:
            await client.send_message(
                message.chat.id,
                'Введите user_id и username администратора через запятую и пробел'
            )

            @bot_parse.on_message(filters.text)
            async def get_user_create(
                client: Client,
                message: Message
            ):
                obj = await validate_data_on_create(message.text)
                if not obj:
                    await client.send_message(
                        message.chat.id,
                        'Ошибка при валидации данных'
                    )
                else:
                    if not await create_admin(obj):
                        await client.send_message(
                            message.chat.id,
                            'Админ с таким user_id уже существует'
                        )
                    else:
                        await client.send_message(
                            message.chat.id,
                            'Новый админ создан'
                        )

    @bot_parse.on_message(filters.regex(Commands.del_admin.value))
    async def del_admin(
        client: Client,
        message: Message
    ):
        if not await check_superuser(message.from_user.id):
            await client.send_message(
                message.chat.id, 'Удалить админа может только суперпользователь!')
        else:
            await client.send_message(
                message.chat.id,
                'Введите user_id администратора'
            )

            @bot_parse.on_message(filters.text)
            async def get_user_delete(
                client: Client,
                message: Message
            ):
                obj = await validate_data_on_delete(message.text)
                if not obj:
                    await client.send_message(
                        message.chat.id,
                        'Ошибка при валидации данных'
                    )
                else:
                    if not await delete_admin(obj):
                        await client.send_message(
                            message.chat.id,
                            'Админ с таким user_id не существует'
                        )
                    else:
                        await client.send_message(
                            message.chat.id,
                            f'Админ с user_id {obj} удален'
                        )

    @bot_parse.on_message(filters.regex(Commands.all_admins.value))
    async def all_admins(
        client: Client,
        message: Message
    ):
        if not await check_superuser(message.from_user.id):
            await client.send_message(
                message.chat.id, 'Получить список админов может только суперпользователь!')
        else:
            admins_list = await get_all_admins()
            reply_message = ''
            for adm in admins_list:
                reply_message += (f'User_id админа: {adm.user_id}, '
                                  f'username: {adm.username}\n')
            await client.send_message(
                message.chat.id,
                reply_message
            )


@bot_parse.on_message(filters.regex(Commands.collect_data.value))
async def data_collection_buttons(
    client: Client,
    message: Message
):
    """Действия, связанные со сбором данных."""

    await client.send_message(
        message.chat.id,
        text='Выберите действие',
        reply_markup=data_collection_keyboard
    )

    @bot_parse.on_message(filters.regex(Commands.run_data_collection.value))
    async def parse_channel(
        client: Client,
        message: Message
    ):
        if not await check_admin(message.from_user.id):
            await client.send_message(
                message.chat.id, 'Собирать данные может только админ!')
        else:
            await client.send_message(
                message.chat.id,
                'Введите chat_id канала или группы '
            )

            @bot_parse.on_message(filters.text)
            async def parsing_info(client: Client, message: Message):
                channel = GetParticipantInfo(
                    client, message.text
                    )
                member_list = await channel.get_members_channel()
                total_members = await channel.get_members_count()
                async with Aiogoogle(
                    service_account_creds=Config.CREDENTIALS
                ) as wrapper_services:
                    spreadsheet_id = await check_spreadsheet_exist(
                        wrapper_services, Config.CHANNEL_ID
                    )
                    if not spreadsheet_id:
                        spreadsheet_id, sheet_name = await create_spreadsheet(
                            wrapper_services, Config.CHANNEL_ID
                        )
                    else:
                        sheet_name = await create_sheet(
                            wrapper_services, spreadsheet_id
                        )
                    await spreadsheet_update_values(
                        wrapper_services, spreadsheet_id,
                        member_list, sheet_name
                    )
                    await client.send_message(
                        message.chat.id,
                        "Информация успешно собрана. Ссылка на файл:"
                        f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}'
                    )


# @bot_parse.on_message(filters.command('parsing_count'))
# async def parsing_count(client: Client, message: Message):
#     chat_id = message.chat.id
#     user_count = await get_users_channels(client)
#     await client.send_message(chat_id, f"Собрано информации о {user_count} пользователях.")
