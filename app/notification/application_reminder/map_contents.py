from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

from config import Config
from flask import current_app

if TYPE_CHECKING:
    from app.notification.model.notification import Notification


@dataclass
class ApplicationReminder:
    contact_info: str
    fund_name: str
    round_name: str
    reference: str
    deadline_date: str
    
    @classmethod
    def format_deadline_date(cls, date):
            return datetime.strptime(
                date, "%Y-%m-%d %H:%M:%S"
            ).strftime("%Y-%m-%d")

    @classmethod
    def from_notification(cls,notification: Notification):
        """Function calls Application class to map
        application contents.

        Args:
            data: Takes an instance of Notification class.

        Returns:
            Application object containing application contents.
        """
        current_app.logger.info(
            f"Mapping contents for {notification.template_type}"
        )
        application_data = notification.content['application']
        return ApplicationReminder(
            contact_info=notification.contact_info,
            deadline_date=cls.format_deadline_date(application_data.get("deadline_date")),
            fund_name=Config.FUND_NAME,
            round_name=application_data.get("round_name"),
            reference=application_data.get("reference"),
        )
