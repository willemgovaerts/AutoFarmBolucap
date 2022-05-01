import os
from datetime import datetime, timezone, timedelta
import random

import requests

from auth import auth_token
from initialize import read_conf, content_header

BASE_URL = os.environ.get("BASE_URL")


def random_measurement(time, **kwargs):
    bouts = random.randint(0, 2)
    m = {
        "time": time.timestamp(),
        "status": [random.randint(0, 1) for _ in range(15)],
        "activity": [random.randint(0, 3) for _ in range(15)],
        "contractions": [random.randint(0, 5) for _ in range(15)],
        "movement": random.randint(0, 99),
        "drinking_amount": bouts * random.randint(0, 10),
        "drinking_bouts": bouts,
        "temperature": random.random() * 2 + 38
    }
    m.update(kwargs)
    return m


def get_measurement(goat, global_start):
    hours_since_epoch = int(global_start.timestamp() / 60 / 60)
    start = global_start + timedelta(minutes=goat['offset'])
    ear_mark = goat['earmark']
    if ear_mark == "constant":
        measurement = {
            "time": start.timestamp(),
            "status": [i % 2 for i in range(15)],
            "activity": [i % 4 for i in range(15)],
            "contractions": [i % 5 for i in range(15)],
            "movement": 69,
            "drinking_amount": 20,
            "drinking_bouts": 4,
            "temperature": 39.5
        }
    elif ear_mark == "1/5 fall out":
        if hours_since_epoch % 5 == 0:
            measurement = random_measurement(start)
        else:
            measurement = None
    elif ear_mark == "random fall out (5%)":
        if random.random() >= 0.05:
            measurement = random_measurement(start)
        else:
            measurement = None
    elif ear_mark == "random-healthy":
        measurement = random_measurement(start)
    elif ear_mark == "random-fever-1/10":
        temp = random.random() * 2.2 + 37.9
        measurement = random_measurement(start, temperature=temp)
        assert measurement['temperature'] == temp
    else:
        print(f"Earmark not found, ear_mark: {ear_mark}")
    return measurement


def write_data(measurement, bolus, token):
    headers = {"Authorization": "token " + token}
    headers.update(content_header)

    data = [{
        "bolus": bolus,
        "measurements": [
            measurement
        ]
    }]
    response = requests.post(BASE_URL + 'measurements/', json=data, headers=headers)
    print(f"{datetime.now()}: status code: {response.status_code}\n data:{response.content}")


def main(filename):
    data = read_conf(filename)
    farm_info = data['FarmInfo']
    boxes = farm_info['boxes']
    goats = farm_info['goats']
    global_start = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0) - timedelta(hours=1)
    box_tokens = [auth_token(box['id'], box['password']) for box in boxes]
    for goat in goats:
        measurement = get_measurement(goat, global_start)
        if measurement is None:
            continue
        box_token = box_tokens[goat['box']]
        write_data(measurement, goat['bolus']['id'], box_token)


if __name__ == '__main__':
    file_name = os.environ.get("CONF_FILE")
    main(file_name)
