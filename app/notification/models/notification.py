import json
from dataclasses import dataclass

from app.config import API_KEY
from app.config import MAGIC_LINK_TEMPLATE_ID
from app.notification.models.data import fund_name
from app.notification.models.data import get_example_data
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
        if "" not in data.values() and None not in data.values():

            notification_data = Notification(
                template_type=data["type"],
                contact_info=data["to"],
                content=data["content"],
            )

            return notification_data

    @staticmethod
    def send_magic_link(json_data):

        try:
            data = Notification.process_notification_data(json_data)
            response = notifications_client.send_email_notification(
                email_address=data.contact_info,
                template_id=MAGIC_LINK_TEMPLATE_ID,
                personalisation={
                    "name of fund": fund_name(data.content["fund_name"]),
                    "link to application": data.content["magic_link_url"],
                    "contact details": (
                        "dummy_contact_info@funding-service-help.com"
                    ),
                },
            )
            return response

        except (TypeError, KeyError, AttributeError):
            example_data = json.dumps(get_example_data(), indent=2)
            return (
                "Incorrect data, please check the contents of the notification"
                f" data.\n\n Example data: {example_data}"
            )

    @staticmethod
    def send_notification(contact_info, content):
        pass

    @staticmethod
    def send_reminder(contact_info, content):
        pass

    @staticmethod
    def send_award(contact_info, content):
        pass
