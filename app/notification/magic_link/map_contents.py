from app.notification.model.exceptions import NotificationError
from tests.test_magic_link.magic_link_data import (
    expected_magic_link_data,
)


class ProcessMagicLinkData:
    """
    Class is set up to map data
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
            raise NotificationError(
                message=(
                    "Incorrect MAGIC LINK data, please check the contents of"
                    " the MAGIC LINK data. \nExample data:"
                    f"{expected_magic_link_data}"
                )
            )
