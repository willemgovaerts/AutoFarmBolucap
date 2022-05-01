import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("BASE_URL")
if BASE_URL is None:
    raise KeyError("Please set BASE_URL environment variable")


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
