import requests

from . import models


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


def log_order_status(order, order_status, payment_status, message):
    log = models.GolfBookingOrderStatusLog()
    log.order = order
    log.order_status = order_status
    log.payment_status = payment_status
    log.message = message
    log.save()
