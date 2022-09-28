from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from flask import current_app
from fsd_utils.config.notify_constants import NotifyConstants

if TYPE_CHECKING:
    from app.notification.model.notification import Notification


@dataclass
class MagicLink:
    contact_info: str
    fund_name: str
    magic_link: str
    request_new_link_url: str
    contact_help_email: str

    @staticmethod
    def from_notification(notification: Notification):
        """Function calls MagicLink class to map
        application contents.

        Args:
            data: Takes an instance of Notification class.

        Returns:
            MagicLink class object containing magic link contents.
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
    def process_data(notification: Notification) -> dict:
        """Function checks if the fund_name exists in the notification
        class object. If no, then adds the fund_name as "FUNDS"

        Args:
            data (dict): takes instance of Notification class
        """
        notification.content.update(
            {
                NotifyConstants.FIELD_FUND_NAME: notification.content.get(
                    NotifyConstants.FIELD_FUND_NAME, "Funds"
                )
            }
        )
        return notification
