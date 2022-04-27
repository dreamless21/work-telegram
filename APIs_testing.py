import requests
import json


#kiss, (wave for welcome is good idea),blush, pout,


def get_something():
    url = 'https://nekos.best/api/v2/slap'
    res = json.loads(requests.get(url).text)
    return res


def search_anime(file_path):
    url = 'https://api.trace.moe/search'
    headers = {'Content-Type': 'image/jpeg'}
    res = json.loads(requests.post(url, data=open(f'{file_path}', 'rb'), headers=headers).text)
    name = res['result'][0]['filename'].split('.')[:-1]
    return name
