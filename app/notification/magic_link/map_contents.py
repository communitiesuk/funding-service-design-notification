from dataclasses import dataclass

from app.notification.model.notification import Notification


@dataclass
class MagicLink:
    contact_info: str
    fund_name: str
    magic_link: str
    request_new_link_url: str
    contact_help_email: str

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
        content = MagicLink.process_data(json_data).get("content")
        return MagicLink(
            contact_info=data.contact_info,
            fund_name=content.get("fund_name"),
            magic_link=content.get("magic_link_url"),
            request_new_link_url=content.get("request_new_link_url"),
            contact_help_email=content.get("contact_help_email"),
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
