import requests
from django.conf import settings


def JobberwockyExteneralJobs(params=None):
    if not settings.SOURCE_EXTERN:
        return {'Status': 'Error', 'Response': {}}

    if params:
        url = f'{settings.SOURCE_EXTERN}?{params}'
    else:
        url = settings.SOURCE_EXTERN

    try:
        response = requests.get(url)
    except:
        return {'Status': 'Error', 'Response': {}}

    if response.status_code == 200:
        return {'Status': 'Ok', 'Response': response.json()}
    else:
        return {'Status': 'Error', 'Response': {}}
