from app.notification.model.notification_utils import convert_bool_value
import uuid
from flask import current_app

class MultiInput:
    
    @classmethod
    def format_values(cls, value, index):
        indent = " " * 5
        return f"{indent}. {value}" if index != 1 else f". {value}"

    @classmethod
    def format_keys_and_values(cls, key, value, index):
        indent = " " * 5

        return (
            f"{indent}. {key}: {'; '.join(map(str, convert_bool_value(value))) if isinstance(value, list) else convert_bool_value(value)}"  # noqa
            if index != 1
            else (
                f". {key}:"
                f" {'; '.join(map(str, convert_bool_value(value))) if isinstance(value, list) else convert_bool_value(value)}"  # noqa
            )
        )

    @classmethod
    def process_data(cls,data):
        output = []
        indent = " " * 5

        for index, (key, value) in enumerate(data.items(), start=1):
            try:
                if isinstance(key, str) and uuid.UUID(key, version=4):
                    output.append(cls.format_values(value, index))

            except:  # noqa
                if (
                    isinstance(value, list)
                    and len(value) > 0
                    and isinstance(value[0], dict)
                ):
                    formatted_value = []
                    for inner_items in value:

                        for k, v in inner_items.items():
                            for iso_keys in ["date", "month", "year"]:
                                try:
                                    if iso_keys in k.split("__"):

                                        formatted_value.append(f"{iso_keys}: {v}")
                                        break
                                except:  # noqa

                                    formatted_value.append(
                                        ", ".join(
                                            map(
                                                lambda item: ", ".join(
                                                    [
                                                        f"{k}: {v}"
                                                        for k, v in item.items()
                                                    ]
                                                ),
                                                value,
                                            )
                                        )
                                    )
                    output.append(
                        f"{indent}. {key}: {formatted_value}"
                        if index != 1
                        else f". {key}: {formatted_value}"
                    )
                else:
                    output.append(cls.format_keys_and_values(key, value, index))

        return output
