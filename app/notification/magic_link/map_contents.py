from dataclasses import dataclass

from flask import current_app
from fsd_utils.config.notify_constants import NotifyConstants


@dataclass
class MagicLink:
    contact_info: str
    fund_name: str
    magic_link: str
    request_new_link_url: str
    contact_help_email: str

    @staticmethod
    def contents(data):
        """Function calls MagicLink class to map
        the application contents.

        Args:
            data: Takes incoming json_data & converts into class object
            from Notification.from_json

        Returns:
            MagicLink object with magic link contents.
        """
        current_app.logger.info(f"Mapping contents for {data.template_type}")

        return MagicLink(
            contact_info=data.contact_info,
            fund_name=data.content.get(
                NotifyConstants.MAGIC_LINK_FUND_NAME_FIELD
            ),
            magic_link=data.content.get(NotifyConstants.MAGIC_LINK_URL_FIELD),
            request_new_link_url=data.content.get(
                NotifyConstants.MAGIC_LINK_REQUEST_NEW_LINK_URL_FIELD
            ),
            contact_help_email=data.content.get(
                NotifyConstants.MAGIC_LINK_CONTACT_HELP_EMAIL_FIELD
            ),
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
        data.content.update(
            {
                NotifyConstants.FIELD_FUND_NAME: data.content.get(
                    NotifyConstants.FIELD_FUND_NAME, "Funds"
                )
            }
        )
        return data
