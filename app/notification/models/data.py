import json
import os

from app.config import FLASK_ROOT


def get_example_data() -> dict:
    example_data = os.path.join(
        FLASK_ROOT, "app", "notification", "models", "example_data.json"
    )
    with open(example_data) as notification_data:
        data = json.load(notification_data)
        return data
