from dataclasses import dataclass

from app.notification.model.notifier import Notifier
from app.notification.model.response import template_type_error
from flask import current_app
from fsd_utils.config.notify_constants import NotifyConstants


@dataclass
class Notification:
    template_type: str
    contact_info: str
    contact_name: str
    content: dict

    @staticmethod
    def from_json(data: dict):
        """
        Function will be  called in relevant services to map
        json contents
        """
        current_app.logger.info(f"Application's raw json: {data}")
        notification_data = Notification(
            template_type=data.get("type"),
            contact_info=data.get("to"),
            contact_name=data.get("full_name", ""),
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
            case NotifyConstants.TEMPLATE_TYPE_MAGIC_LINK:
                current_app.logger.info(
                    f"Validating template type: {notification.template_type}"
                )
                return Notifier.send_magic_link(notification)

            case NotifyConstants.TEMPLATE_TYPE_APPLICATION:
                current_app.logger.info(
                    f"Validating template type: {notification.template_type})"
                )
                return Notifier.send_submitted_application(notification)

            case NotifyConstants.TEMPLATE_TYPE_INCOMPLETE_APPLICATION:
                current_app.logger.info(
                    f"Validating template type: {notification.template_type})"
                )
                return Notifier.send_incomplete_application(notification)

            case NotifyConstants.TEMPLATE_TYPE_REMINDER:
                current_app.logger.info(
                    f"Validating template type: {notification.template_type})"
                )
                return Notifier.send_application_reminder(notification)

            case NotifyConstants.TEMPLATE_TYPE_EOI_PASS:
                current_app.logger.info(
                    f"Validating template type: {notification.template_type})"
                )
                return Notifier.send_submitted_eoi(
                    notification=notification,
                    template_name=NotifyConstants.TEMPLATE_TYPE_EOI_PASS,
                )

            case NotifyConstants.TEMPLATE_TYPE_EOI_PASS_W_CAVEATS:
                current_app.logger.info(
                    f"Validating template type: {notification.template_type})"
                )
                return Notifier.send_submitted_eoi(
                    notification=notification,
                    template_name=NotifyConstants.TEMPLATE_TYPE_EOI_PASS_W_CAVEATS,
                )

            case "NOTIFICATION" | "AWARD":
                return f"Currently {notification.template_type} service is not available."  # noqa

            case _:
                current_app.logger.exception(
                    f"Incorrect template type {notification.template_type}"
                )
                return template_type_error(json_data)
