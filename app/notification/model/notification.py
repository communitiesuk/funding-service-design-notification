from dataclasses import dataclass

from app.notification.application.map_contents import Application
from app.notification.magic_link.map_contents import MagicLink
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
        the json contents
        """
        notification_data = Notification(
            template_type=data.get("type"),
            contact_info=data.get("to"),
            content=data.get("content"),
        )
        return notification_data

    @staticmethod
    def process_data(json_data):
        data = Notification.from_json(json_data)
        match data.template_type:

            case NotifyConstants.TEMPLATE_TYPE_MAGIC_LINK:
                return MagicLink.from_json(data)

            case "APPLICATION_RECORD_OF_SUBMISSION":
                return Application.from_json(data)

            case _:
                current_app.logger.exception(
                    f"Incorrect template type {json_data.get('type')}"
                )
                return template_type_error(json_data)
