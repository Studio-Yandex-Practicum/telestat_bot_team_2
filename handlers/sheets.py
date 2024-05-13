from pprint import pprint
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = 'd:/creds.json'

spreadsheet_id = '1MKcQz7s2DrTiiFWPEO0WiTvpK9SoIcZkf2v075EDGdQ'

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scopes=scopes)
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)


def get_values():
    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='A1:E10',
        majorDimension='COLUMNS'
    ).execute()
    return str(len(values['values'][0][2:]))

pprint(get_values())
