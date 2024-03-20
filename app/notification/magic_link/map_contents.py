from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from app.notification.notification_contents_base_class import (
    _NotificationContents,
)
from flask import current_app
from fsd_utils.config.notify_constants import NotifyConstants

if TYPE_CHECKING:
    from app.notification.model.notification import Notification

from config import Config


@dataclass
class MagicLink(_NotificationContents):
    magic_link: str
    request_new_link_url: str
    contact_help_email: str
    reply_to_email_id: str

    @classmethod
    def from_notification(cls, notification: Notification):
        """Function calls MagicLink class to map
        application contents.

        Args:
            data: Takes an instance of Notification class.

        Returns:
            MagicLink class object containing magic link contents.
        """
        current_app.logger.info(f"Mapping contents for {notification.template_type}")

        return cls(
            contact_info=notification.contact_info,
            contact_name=notification.contact_name,
            fund_name=notification.content.get(
                NotifyConstants.MAGIC_LINK_FUND_NAME_FIELD
            ),
            magic_link=notification.content.get(NotifyConstants.MAGIC_LINK_URL_FIELD),
            request_new_link_url=notification.content.get(
                NotifyConstants.MAGIC_LINK_REQUEST_NEW_LINK_URL_FIELD
            ),
            contact_help_email=notification.content.get(
                NotifyConstants.MAGIC_LINK_CONTACT_HELP_EMAIL_FIELD
            ),
            reply_to_email_id=Config.REPLY_TO_EMAILS_WITH_NOTIFY_ID[
                notification.content.get(
                    NotifyConstants.MAGIC_LINK_CONTACT_HELP_EMAIL_FIELD
                )
            ],
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
