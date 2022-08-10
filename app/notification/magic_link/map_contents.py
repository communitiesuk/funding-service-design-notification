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
        """Function calls MagicLink class to map
        the application contents.

        Args:
            data: Takes incoming json_data & converts into class object
            from Notification.from_json

        Returns:
            MagicLink object with magic link contents.
        """
        data = Notification.from_json(json_data)
        processed_data = MagicLink.process_data(json_data)
        return MagicLink(
            contact_info=data.contact_info,
            fund_name=processed_data["content"]["fund_name"],
            magic_link=data.content["magic_link_url"],
        )

    @staticmethod
    def process_data(data: dict) -> dict:
        """Function process the incoming json for magic link
        such as if the fund name is not provided by the user then 
        by default function adds the fund name as "FUNDS"
        
        Args:
            data (dict): takes the json
            
        Returns:
           data(dict): returns processed json 
        """
        data["content"].update(
            {"fund_name": data["content"].get("fund_name", "Funds")}
        )
        return data

     