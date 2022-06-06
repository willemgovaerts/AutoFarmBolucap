import datetime
import json

import pandas as pd
import requests

from initialize import content_header, BASE_URL


def combine_posture(list_lying, list_standing):
    return list_standing


def combine_gastric(eating, normal, ruminating, unhealthy):
    result = []
    for i in range(15):
        result.append(eating[i] + 2 * ruminating[i] + 3 * unhealthy[i])
    return result


def convert_data_to_json(data):
    all_data = []
    for i, row in data.iterrows():
        row_data = {
            "time": int(i.tz_localize("Europe/Brussels").timestamp()),
            "contractions": json.loads(row.contractions),
            "temperature": row.temperature,
            "movement": row.activity,
            "drinking_bouts": row.bouts,
            "drinking_amount": row.amount,
            "status": combine_posture(json.loads(row.posture_lying), json.loads(row.posture_standing)),
            "activity": combine_gastric(json.loads(row.gastric_eating), json.loads(row.gastric_normal),
                                        json.loads(row.gastric_ruminating), json.loads(row.gastric_unhealthy)),
        }
        all_data.append(row_data)
    return all_data

def get_data_goat(goat_data_id):
    bolus_ids = {
        15: 2927042,
        16: 3761110,
        17: 2938419
    }
    df = pd.read_csv(f"data/cleaned_{goat_data_id}.csv", index_col=0)
    df.index = pd.to_datetime(df.index)
    return {
        "bolus": bolus_ids[goat_data_id],
        "measurements": convert_data_to_json(df),
    }

def write_data():
    box_token = "3fa5c3aa9c2d5bc19948d8adb8d975ae10b4a130"
    goats = [15, 16, 17]
    data = []
    for goat in goats:
        data.append(get_data_goat(goat))
    print(data)

    headers = {"Authorization": "token " + box_token}
    headers.update(content_header)

    response = requests.post(BASE_URL + 'measurements/', json=data, headers=headers)
    print(f"{datetime.datetime.now()}: status code: {response.status_code}\n data:{response.content}")

if __name__ == "__main__":
    write_data()