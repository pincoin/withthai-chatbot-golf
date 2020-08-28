import requests


def verify_access_token(access_token):
    response = requests.get('https://api.line.me/oauth2/v2.1/verify', params={
        'access_token': access_token,
    })

    return response.json() if response.status_code == 200 else False


def get_profile(access_token):
    response = requests.get('https://api.line.me/v2/profile', headers={
        'Authorization': f'Bearer {access_token}',
    })

    return response.json() if response.status_code == 200 else False
