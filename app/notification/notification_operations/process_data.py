import json

from app.config import API_KEY
from app.config import APPLICATION_RECORD_TEMPLATE_ID
from app.config import MAGIC_LINK_TEMPLATE_ID
from app.notification.application_submission.map_contents import (
    ApplicationData,
)
from app.notification.magic_link.map_contents import ProcessMagicLinkData
from app.notification.notification_operations.custom_exceptions import (
    NotificationError,
)
from app.notification.notification_operations.data import get_example_data
from app.notification.notification_operations.initialise_data import (
    NotificationData,
)
from notifications_python_client import NotificationsAPIClient


notifications_client = NotificationsAPIClient(API_KEY)


class NotificationOperations:
    """Class holds notification operations"""

    @staticmethod
    def send_magic_link(json_data):
        """Function maps data eg. magic link along with other
        expected contents to the user as expected by the
        govuk-notify-service template.

        INFO: process_json_data checks if any key eg "fund_name" or any
        other keys, values are missing. If so it adds the "fund_name"
        key etc & assigns value to default value.
        """
        process_json_data = ProcessMagicLinkData.process_data(json_data)
        try:
            data = NotificationData.notification_data(process_json_data)
            response = notifications_client.send_email_notification(
                email_address=data.contact_info,
                template_id=MAGIC_LINK_TEMPLATE_ID,
                personalisation={
                    "name of fund": data.content["fund_name"],
                    "link to application": data.content["magic_link_url"],
                    "contact details": (
                        "dummy_contact_info@funding-service-help.com"
                    ),
                },
            )
            return response

        except (TypeError, KeyError, AttributeError):
            example_data = json.dumps(get_example_data(), indent=2)
            raise NotificationError(
                message=(
                    "Incorrect data, please check the contents of the"
                    f" magic link data.\n\n Example data: {example_data}"
                )
            )

    @staticmethod
    def send_application(json_data):
        """Function maps data eg. questions/answers along with other
        expected contents to the user as expected by the
        govuk-notify-service template.

        Raises error if any of the required  contents are incorrect
        or missing.
        """
        try:
            data = ApplicationData.from_json(json_data)
            response = notifications_client.send_email_notification(
                email_address=data.contact_info,
                template_id=APPLICATION_RECORD_TEMPLATE_ID,
                personalisation={
                    "name of fund": data.fund_name,
                    "application id": data.application_id,
                    "date submitted": data.format_submission_date,
                    "round name": data.fund_round,
                    "question": data.questions,
                },
            )
            return response

        except (TypeError, KeyError, AttributeError):
            example_data = json.dumps(get_example_data(), indent=2)
            raise NotificationError(
                message=(
                    "Incorrect data, please check the contents of the"
                    f" application data.\n\n Example data: {example_data}"
                )
            )

    @staticmethod
    def send_notification(json_data):
        pass

    @staticmethod
    def send_reminder(json_data):
        pass

    @staticmethod
    def send_award(json_data):
        pass
