from app.notification.model.exceptions import NotificationError
from app.notification.model.response import magic_link_key_error
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
    def process_data(data: dict):
        try:
            data["content"].update(
                {"fund_name": data["content"].get("fund_name", "Funds")}
            )
            return data

        except KeyError:
            raise NotificationError(
                message=magic_link_key_error(expected_magic_link_data)
            )
