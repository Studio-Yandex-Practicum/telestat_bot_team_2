from datetime import datetime

from settings import Config


async def set_user_permissions(wrapper_services, spreadsheetId):
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': Config.EMAIL
    }
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetId,
            json=permissions_body,
            fields='id'
        ))


async def check_spreadsheet_exist(wrapper_services, title):
    service = await wrapper_services.discover('drive', 'v3')
    responce = await wrapper_services.as_service_account(
        service.files.list(
            q='mimeType="application/vnd.google-apps.spreadsheet"'
        )
    )
    for file in responce['files']:
        if file['name'] == title:
            return file['id']


async def create_sheet(wrapper_services, spreadsheet_id):
    sheet_name = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    service = await wrapper_services.discover('sheets', 'v4')
    requests = [{
        'addSheet': {
            'properties': {
                'sheetType': 'GRID',
                'title': sheet_name
            }
        }
    }]
    body = {
        'requests': requests
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.batchUpdate(
            spreadsheetId=spreadsheet_id,
            json=body
        )
    )
    return sheet_name


async def create_spreadsheet(wrapper_services, title):
    sheet_name = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {
            'title': title,
            'locale': 'ru_RU'
        },
        'sheets': [{
            'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': sheet_name
            }
        }]
    }
    responce = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetId = responce['spreadsheetId']
    await set_user_permissions(wrapper_services, spreadsheetId)
    return spreadsheetId, sheet_name


async def spreadsheet_update_values(
    wrapper_services, spreadsheetId, data, sheet_name
):
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [[], [
        'ID',
        'username',
        'First Name',
        'Last Name',
        'Is Bot',
        'Joined Date',
        'Profile Photo File ID',
        'Phone number',
        'Language code',
        'Country'
    ]]
    for user in data:
        table_values.append([
            user['ID'],
            user['Username'],
            user['First Name'],
            user['Last Name'],
            user['Is Bot'],
            user['Joined Date'],
            user['Profile Photo File ID'],
            user['Phone number'],
            user['Language code'],
            user['Country']
        ])
    request_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetId,
            range=f'{sheet_name}!A1:M{2 + len(data)}',
            valueInputOption='USER_ENTERED',
            json=request_body
        )
    )
