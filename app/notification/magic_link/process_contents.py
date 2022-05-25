import json

from app.notification.custom_exceptions import NotificationError
from app.notification.models.data import get_example_data


class ProcessMagicLinkData:
    """
    Class is set up for processing the data
    from notification data contents.

    Returns: notification data or updated notification data
    to map out with expected contents. If any of the key such as
    "fund_name" is missing from expected contents, it adds the the
    key eg "fund_name" and assign value to default value.
    """

    @staticmethod
    def process_data(data):
        try:
            data["content"].update(
                {"fund_name": data["content"].get("fund_name", "Funds")}
            )
            return data

        except KeyError:
            example_data = json.dumps(get_example_data(), indent=2)
            raise NotificationError(
                message=(
                    "Incorrect data, please check the contents of the"
                    f" notification data.\n\n Example data: {example_data} "
                )
            )
