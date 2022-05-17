import json
from dataclasses import dataclass

from app.config import API_KEY
from app.config import MAGIC_LINK_TEMPLATE_ID
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
                    "name of fund": "Funding service.",
                    "link to application": data.content,
                    "contact details": (
                        "dummy_contact_info@funding-service-help.com"
                    ),
                },
            )
            return response

        except (TypeError, KeyError, AttributeError):
            example_data = json.dumps(get_example_data(), indent=2)
            return (
                "Bad request, please check the contents of the notification"
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

    @staticmethod
    def send_application_record(json_data):
        """
        To be worked on mapping the application data & email
        applicant with following contents:

        1. Question and corresponding answer
        2. Timestamp of submission (in a readable format, not EPOCH)
        3. Fund name
        4. Fund round
        5. Application ID
        6. A hash "receipt"

        """
        try:
            data = Notification.process_notification_data(json_data)
            response = notifications_client.send_email_notification(
                email_address=data.contact_info,
                template_id=MAGIC_LINK_TEMPLATE_ID,
                personalisation={
                    "SUBJECT": "Application submission record",
                    "APPLICATION": (
                        "Add logic function to retrieve the application data"
                    ),
                },
            )
            return response

        except (TypeError, KeyError, AttributeError):
            example_data = json.dumps(get_example_data(), indent=2)
            return (
                "Bad request, please check the contents of the notification"
                f" data.\n\n Example data: {example_data}"
            )
