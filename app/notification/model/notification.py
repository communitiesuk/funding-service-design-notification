from dataclasses import dataclass

from app.notification.application.map_contents import Application
from app.notification.magic_link.map_contents import MagicLink
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
                current_app.logger.debug(
                    "Second step - connect data with MAGIC_LINK service class"
                    " to  process contents"
                )
                return MagicLink.from_json(data)

            case "APPLICATION_RECORD_OF_SUBMISSION":
                current_app.logger.info(
                    "Second step - connect data with APPLICATION service"
                    " class to  process_data"
                )
                return Application.from_json(data)

            case "NOTIFICATION" | "REMINDER" | "AWARD":
                return f"Currently {data.get('type')} service is not available."  # noqa

            case _:
                return "Incorrect template type - testing"
