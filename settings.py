import os

from dotenv import load_dotenv


load_dotenv()


class Config(object):
    """Конфигурация проекта."""

    DB_URL = os.getenv('DB_URL')
    API_ID = os.getenv('API_ID')
    API_HASH = os.getenv('API_HASH')
    BOT_TOKEN = os.getenv('BOT_TOKEN_PARSE')
    MY_ID = os.getenv('MY_ID')
    MY_USERNAME = os.getenv('MY_USERNAME')
    

    BOT_TOKEN_INFO = os.getenv('BOT_TOKEN_INFO')
    API_HASH_INFO = os.getenv('API_HASH_INFO')
    API_ID_INFO = os.getenv('API_ID_INFO')
