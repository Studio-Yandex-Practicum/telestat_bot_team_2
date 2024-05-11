import os

from dotenv import load_dotenv
from aiogoogle.auth.creds import ServiceAccountCreds

load_dotenv()

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


class Config(object):
    """Конфигурация проекта."""

    DB_URL = os.getenv('DB_URL')
    API_ID = os.getenv('API_ID')
    API_HASH = os.getenv('API_HASH')
    BOT_TOKEN = os.getenv('BOT_TOKEN_PARSE')
    MY_ID = os.getenv('MY_ID')
    MY_USERNAME = os.getenv('MY_USERNAME')
    CHANNEL_ID = os.getenv('CHANNEL_ID')
    CREDENTIALS = ServiceAccountCreds(
        scopes=SCOPES, **INFO
    )
