from dataclasses import dataclass

from app.notification.models.data import get_data


@dataclass
class Notification:
    """
    Class processes notification data.
    Returns:
        notification class object.
    """

    template_type: str
    contact_info: str
    content: str

    @staticmethod
    def process_notification_data(json_data):
        data = get_data(json_data)
        if (
            "type" in data.keys()
            and "to" in data.keys()
            and "content" in data.keys()
        ):
            notification_data = Notification(
                template_type=data.get("type"),
                contact_info=data.get("to"),
                content=data.get("content"),
            )

            return notification_data
        else:
            return None
