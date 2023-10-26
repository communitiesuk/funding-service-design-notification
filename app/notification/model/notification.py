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
        current_app.logger.info(f"Application's raw json: {data}")
        notification = Notification(
            template_type=data.get("type"),
            contact_info=data.get("to"),
            content=data.get("content"),
        )
        return notification

    def email_recipient(self):
        """
        Function matches with the correct template type &
        calls the relevant function.
        """
        match self.template_type:
            case NotifyConstants.TEMPLATE_TYPE_MAGIC_LINK:
                current_app.logger.info(
                    f"Validating template type: {self.template_type}"
                )
                return Notifier.send_magic_link(self)

            case NotifyConstants.TEMPLATE_TYPE_APPLICATION:
                current_app.logger.info(
                    f"Validating template type: {self.template_type})"
                )
                return Notifier.send_submitted_application(self)

            case NotifyConstants.TEMPLATE_TYPE_INCOMPLETE_APPLICATION:
                current_app.logger.info(
                    f"Validating template type: {self.template_type})"
                )
                return Notifier.send_incomplete_application(self)

            case NotifyConstants.TEMPLATE_TYPE_REMINDER:
                current_app.logger.info(
                    f"Validating template type: {self.template_type})"
                )
                return Notifier.send_application_reminder(self)

            case "NOTIFICATION" | "AWARD":
                return f"Currently {notification.template_type} service is not available."  # noqa

            case _:
                current_app.logger.exception(
                    f"Incorrect template type {self.template_type}"
                )
                return template_type_error(self.template_type)
