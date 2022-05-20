from dataclasses import dataclass


@dataclass
class NotificationData:
    """
    Class processes notification data.
    Returns:
        notification class object.
    """

    template_type: str
    contact_info: str
    content: str

    @staticmethod
    def notification_data(data):
        if "" not in data.values() and None not in data.values():
            notification_data = NotificationData(
                template_type=data["type"],
                contact_info=data["to"],
                content=data["content"],
            )

            return notification_data
