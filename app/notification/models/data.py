import json
import os

from app.config import FLASK_ROOT


def get_data(data) -> dict:
    if data:
        return data
    else:
        data = get_local_data()

    return data


def get_local_data() -> dict:
    local_data = os.path.join(
        FLASK_ROOT, "tests", "local_data", "local_data.json"
    )
    with open(local_data) as notification_data:
        data = json.load(notification_data)
        return data
