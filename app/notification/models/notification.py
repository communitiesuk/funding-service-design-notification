from dataclasses import dataclass

from app.config import API_KEY
from app.config import MAGIC_LINK_TEMPLATE_ID
from notifications_python_client.notifications import NotificationsAPIClient

notifications_client = NotificationsAPIClient(API_KEY)


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
    def process_notification_data(data):

        if (
            (
                "type" in data.keys()
                and "to" in data.keys()
                and "content" in data.keys()
            )
            and "" not in data.values()
            and None not in data.values()
        ):
            notification_data = Notification(
                template_type=data.get("type"),
                contact_info=data.get("to"),
                content=data.get("content"),
            )

            return notification_data

    @staticmethod
    def send_magic_link(contact_info, content):
        response = notifications_client.send_email_notification(
            email_address=contact_info,
            template_id=MAGIC_LINK_TEMPLATE_ID,
            personalisation={
                "SUBJECT": "Funding service access link",
                "MAGIC_LINK": content,
            },
        )
        return response

    @staticmethod
    def send_notification(contact_info, content):
        pass

    @staticmethod
    def send_reminder(contact_info, content):
        pass

    @staticmethod
    def send_award(contact_info, content):
        pass
