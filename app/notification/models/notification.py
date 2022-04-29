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
        notification_data = Notification(
            template_type=data["type"],
            contact_info=data["to"],
            content=data["content"],
        )

        return notification_data
