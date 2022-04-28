import json

import requests

BASE_URL = "http://localhost:8080/"


def login(username, password):
    result = requests.post(BASE_URL + 'login/', json={"username": username, "password": password},
                           headers={'Content-type': 'application/json'})
    if result.status_code != 200:
        print(f"Invalid status code {result.status_code} with response: {result}")
        return None
    return json.loads(result.content)['token']


def auth_token(username, password):
    result = requests.post(BASE_URL + 'api-token-auth/', json={"username": username, "password": password},
                           headers={'Content-type': 'application/json'})
    if result.status_code != 200:
        print(f"Invalid status code {result.status_code} with response: {result}")
        return None
    return json.loads(result.content)['token']
