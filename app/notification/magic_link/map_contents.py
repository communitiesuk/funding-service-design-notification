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
    def from_notification(notification):
        """Function calls MagicLink class to map
        the application contents.

        Args:
            data: Takes incoming json_data & converts into class object
            from Notification.from_json

        Returns:
            MagicLink object with magic link contents.
        """
        current_app.logger.info(
            f"Mapping contents for {notification.template_type}"
        )

        return MagicLink(
            contact_info=notification.contact_info,
            fund_name=notification.content.get(
                NotifyConstants.MAGIC_LINK_FUND_NAME_FIELD
            ),
            magic_link=notification.content.get(
                NotifyConstants.MAGIC_LINK_URL_FIELD
            ),
            request_new_link_url=notification.content.get(
                NotifyConstants.MAGIC_LINK_REQUEST_NEW_LINK_URL_FIELD
            ),
            contact_help_email=notification.content.get(
                NotifyConstants.MAGIC_LINK_CONTACT_HELP_EMAIL_FIELD
            ),
        )

    @staticmethod
    def process_data(notification: dict) -> dict:
        """Function process the incoming json for magic link
        such as if the fund name is not provided by the user then
        by default function adds the fund name as "FUNDS"

        Args:
            data (dict): takes the json

        Returns:
           data(dict): returns processed json
        """
        notification.content.update(
            {
                NotifyConstants.FIELD_FUND_NAME: notification.content.get(
                    NotifyConstants.FIELD_FUND_NAME, "Funds"
                )
            }
        )
        return notification
