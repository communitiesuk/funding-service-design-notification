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


def fund_name(data):
    if data is None or data == "":
        return "Funds"
    else:
        return data


def email_recipient(data: dict, example_data: dict, notification_class):
    if data.get("type") == "MAGIC_LINK":
        magic_link = notification_class.send_magic_link(data)
        return magic_link
    elif data.get("type") == "NOTIFICATION":
        return f"Currently {data.get('type')} service is not available."
    elif data.get("type") == "REMINDER":
        return f"Currently {data.get('type')} service is not available."
    elif data.get("type") == "AWARD":
        return f"Currently {data.get('type')} service is not available."
    else:
        return (
            "Incorrect type, please check the key 'type' from notification "
            f"data: {data}.\n\nExpected type:('MAGIC_LINK'"
            " or 'NOTIFICATION' or 'REMINDER' or 'AWARD' )\n\nExample"
            f" data: {example_data}"
        )
