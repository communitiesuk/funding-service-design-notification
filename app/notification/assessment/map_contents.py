from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from flask import current_app

from app.notification.notification_contents_base_class import _NotificationContents

if TYPE_CHECKING:
    from app.notification.model.notification import Notification


@dataclass
class Assignment(_NotificationContents):
    reference_number: str
    fund_name: str
    project_name: str
    lead_assessor_email: str
    assessment_link: str
    message: str

    @classmethod
    def from_notification(cls, notification: Notification):
        current_app.logger.info(f"Mapping contents for {notification.template_type}")
        return cls(
            contact_info=notification.contact_info,
            contact_name=notification.contact_name,
            fund_name=notification.content.get("fund_name"),
            reference_number=notification.content.get("reference_number"),
            project_name=notification.content.get("project_name"),
            lead_assessor_email=notification.content.get("lead_assessor_email"),
            assessment_link=notification.content.get("assessment_link"),
            message=notification.content.get("message"),
        )
