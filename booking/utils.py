# booking/utils.py

import requests

def get_line_profile(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    response = requests.get('https://api.line.me/v2/profile', headers=headers)

    if response.status_code != 200:
        raise Exception('Failed to get line profile')

    return response.json()