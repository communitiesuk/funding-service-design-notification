import json

from app.notification.models.custom_exceptions import NotificationError
from app.notification.models.data import get_example_data


class ProcessNotificationData:
    """
    Class is set up for processing the data
    from notification data contents.

    Returns: notification data or updated notification data
    to map out with expected contents.
    """

    @staticmethod
    def fund_name(data):
        try:
            if "fund_name" not in data["content"]:
                data["content"].update(fund_name="Funds")
                return data
            else:
                return data

        except KeyError:
            example_data = json.dumps(get_example_data(), indent=2)
            raise NotificationError(
                message=(
                    "Incorrect data, please check the contents of the"
                    f" notification data.\n\n Example data: {example_data} "
                )
            )
