# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import json
import os

import yaml
import requests

from auth import login

BASE_URL = os.environ.get("BASE_URL")
content_header = {'Content-type': 'application/json'}


def read_conf(filename):
    with open(filename, 'r') as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return data





def create_boxes(data, token):
    boxes = data['FarmInfo']['boxes']
    for box in boxes:
        data = {
            "account": {
                "id": box['id'],
                "password": box['password']
            },
            "serial_number": box['serial_number'],
            "farmer": data['FarmInfo']['id'],
            "is_active": box['is_active'],
        }
        headers = {"Authorization": "token " + token}
        headers.update(content_header)
        response = requests.post(BASE_URL + 'users/box/', json=data, headers=headers)
        print(f"status code: {response.status_code}\n data:{response.content}")
    print('\n')


def create_goats(data, token):
    goats = data['FarmInfo']['goats']
    for goat in goats:
        data = {
            "ear_mark": goat['earmark'],
            "sex": goat['sex'],
            "bolus": {
                "id": goat['bolus']['id'],
                "farmer": data['FarmInfo']['id'],
                "mode": goat['bolus']['mode']
            }
        }
        headers = {"Authorization": "token " + token}
        headers.update(content_header)
        response = requests.post(BASE_URL + f'goat/{data["FarmInfo"]["id"]}/goat_and_bolus/', json=data, headers=headers)
        print(f"status code: {response.status_code}\n data:{response.content}")


if __name__ == '__main__':
    file_name = os.environ.get("CONF_FILE")
    data = read_conf(file_name)

    staff_email = data['StaffInfo']['email']
    staff_password = data['StaffInfo']['password']
    staff_token = login(staff_email, staff_password)

    create_boxes(data, staff_token)
    create_goats(data, staff_token)
