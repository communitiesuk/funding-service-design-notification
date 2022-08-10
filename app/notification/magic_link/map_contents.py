from dataclasses import dataclass

from app.notification.model.exceptions import NotificationError
from app.notification.model.notification import Notification
from app.notification.model.response import magic_link_key_error
from tests.test_magic_link.magic_link_data import (
    expected_magic_link_data,
)


@dataclass
class MagicLink:
    contact_info: str
    fund_name: str
    magic_link: str
    contact_details: str = "dummy_contact_info@funding-service-help.com"

    @staticmethod
    def from_json(json_data: dict):
        data = Notification.from_json(json_data)
        fund = MagicLink.process_data(json_data)
        return MagicLink(
            contact_info=data.contact_info,
            fund_name=fund["content"]["fund_name"],
            magic_link=data.content["magic_link_url"],
        )

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
