from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

from flask import current_app

from app.notification.notification_contents_base_class import _NotificationContents
from config import Config

if TYPE_CHECKING:
    from app.notification.model.notification import Notification


@dataclass
class ApplicationReminder(_NotificationContents):
    round_name: str
    reference: str
    deadline_date: str
    contact_help_email: str
    reply_to_email_id: str

    @classmethod
    def format_deadline_date(cls, date):
        return (
            datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
            .strftime(f"{'%d %B %Y'} at {'%I:%M%p'}")
            .replace("AM", "am")
            .replace("PM", "pm")
        )

    @classmethod
    def from_notification(cls, notification: Notification):
        """Function calls Application class to map
        application contents.

        Args:
            data: Takes an instance of Notification class.

        Returns:
            Application object containing application contents.
        """
        current_app.logger.info(f"Mapping contents for {notification.template_type}")
        try:
            application_data = notification.content["application"]
            deadline_date = cls.format_deadline_date(application_data.get("deadline_date"))
            return cls(
                contact_info=notification.contact_info,
                contact_name=notification.contact_name,
                deadline_date=deadline_date,
                fund_name=application_data.get("fund_name"),
                round_name=application_data.get("round_name"),
                reference=application_data.get("reference"),
                contact_help_email=application_data.get("contact_help_email"),
                reply_to_email_id=Config.REPLY_TO_EMAILS_WITH_NOTIFY_ID[application_data["contact_help_email"]],
            )

        except Exception as e:
            current_app.logger.error("Could not map the contents for" f" {notification.template_type} {e}")
