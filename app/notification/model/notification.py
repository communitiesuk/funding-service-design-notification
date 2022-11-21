from dataclasses import dataclass

from app.notification.model.notifier import Notifier
from app.notification.model.response import template_type_error
from flask import current_app
from fsd_utils.config.notify_constants import NotifyConstants


@dataclass
class Notification:
    template_type: str
    contact_info: str
    content: dict

    @staticmethod
    def from_json(data: dict):
        """
        Function will be  called in relevant services to map
        json contents
        """
        notification_data = Notification(
            template_type=data.get("type"),
            contact_info=data.get("to"),
            content=data.get("content"),
        )
        return notification_data

    @staticmethod
    def email_recipient(json_data: dict):
        """
        Function matches with the correct template type &
        calls the relevant function.
        """
        notification = Notification.from_json(json_data)
        match json_data.get("type"):
            case "MAGIC_LINK":
                current_app.logger.info(
                    f"Validating template type: {notification.template_type}"
                )
                return Notifier.send_magic_link(notification)

            case "APPLICATION_RECORD_OF_SUBMISSION":
                current_app.logger.info(
                    f"Validating template type: {notification.template_type})"
                )
                return Notifier.send_submitted_application(notification)

            case "INCOMPLETE_APPLICATION_RECORDS":
                current_app.logger.info(
                    f"Validating template type: {notification.template_type})"
                )
                return Notifier.send_incomplete_application(notification)

            case "APPLICATION_DEADLINE_REMINDER":
                current_app.logger.info(
                    f"Validating template type: {notification.template_type})"
                )
                return Notifier.send_application_reminder(notification)

            case "NOTIFICATION" | "AWARD":
                return f"Currently {notification.template_type} service is not available."  # noqa

            case _:
                current_app.logger.exception(
                    f"Incorrect template type {notification.template_type}"
                )
                return template_type_error(json_data)
