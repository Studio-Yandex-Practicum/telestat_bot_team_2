import os
from pyrogram import Client
from functools import wraps
from aiogoogle.auth.creds import ServiceAccountCreds
import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent
LOG_FORMAT = '#%(levelname)-8s [%(asctime)s] - %(filename)s:'\
             '%(lineno)d - %(name)s - %(message)s'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

INFO = {
    'type':  os.getenv('TYPE'),
    'project_id':  os.getenv('PROJECT_ID'),
    'private_key_id':  os.getenv('PRIVATE_KEY_ID'),
    'private_key':  os.getenv('PRIVATE_KEY').replace('\\n', '\n'),
    'client_email':  os.getenv('CLIENT_EMAIL'),
    'client_id':  os.getenv('CLIENT_ID'),
    'auth_uri':  os.getenv('AUTH_URI'),
    'token_uri':  os.getenv('TOKEN_URI'),
    'auth_provider_x509_cert_url':  os.getenv('AUTH_PROVIDER_X509_CERT_URL'),
    'client_x509_cert_url':  os.getenv('CLIENT_X509_CERT_URL')
}


def configure_logging():
    """Конфигурация логов."""

    log_dir = BASE_DIR / 'logs'
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / 'telestat_bot.log'
    rotating_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 ** 6,
        backupCount=5,
        encoding='utf-8',
    )
    logging.basicConfig(
        datefmt=DT_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler,),
    )


class Config(object):
    """Конфигурация проекта."""

    DB_URL = os.getenv('DB_URL')
    API_ID = os.getenv('API_ID')
    API_HASH = os.getenv('API_HASH')
    BOT_TOKEN = os.getenv('BOT_TOKEN_PARSE')
    MY_ID = os.getenv('MY_ID')
    MY_USERNAME = os.getenv('MY_USERNAME')
    CHANNEL_ID = os.getenv('CHANNEL_ID')
    EMAIL = os.getenv('EMAIL')
    CREDENTIALS = ServiceAccountCreds(
        scopes=SCOPES, **INFO
    )
    MY_PHONE = os.getenv('MY_PHONE')


user_bot = Client(
    'user_acc',
    api_hash=Config.API_HASH,
    api_id=Config.API_ID,
    phone_number=Config.MY_PHONE
)


def bot_user(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        await user_bot.start()
        try:
            result = await func(*args, **kwargs)
            return result
        finally:
            await user_bot.stop()
    return wrapper
