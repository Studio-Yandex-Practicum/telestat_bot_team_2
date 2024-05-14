import logging

import asyncio
from bot_parse import bot_parse
from core.init_db import create_super_user

from settings import configure_logging


def main():
    configure_logging()
    logging.info('Бот запущен!')
    bot_parse.run()
    logging.info('Бот завершил работу.')


loop = asyncio.get_event_loop()
loop.run_until_complete(create_super_user())
loop.run_forever(main())
loop.close()
