import json
import os

from app.config import API_KEY
from app.config import APPLICATION_RECORD_TEMPLATE_ID
from app.config import MAGIC_LINK_TEMPLATE_ID
from app.notification.application_submission.process_contents import (
    ApplicationData,
)
from app.notification.custom_exceptions import NotificationError
from app.notification.magic_link.process_contents import ProcessMagicLinkData
from app.notification.models.data import get_example_data
from app.notification.models.notification import NotificationData
from notifications_python_client import NotificationsAPIClient
from notifications_python_client import prepare_upload

notifications_client = NotificationsAPIClient(API_KEY)


class ProcessNotificationData:
    """class calls notification-client library
    with personalisation contents from govuk-notify service
    to map the data with relevant service.
    Returns mapped data object with relevant govuk-notify-service.

    Raises:
        NotificationError: raises error if required incoming data
        is not correctly formatted or missing.
    """

    @staticmethod
    def send_magic_link(json_data):
        """ Function send a magic link to the user along with other
        expected contents.

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
                    f" notification data.\n\n Example data: {example_data}"
                )
            )

    @staticmethod
    def send_application(json_data):
        """Function calls ApplicationData class object and assign
        values to govuk-notify-service template as expected.
        Uploads application contents ( questions/answers) from txt file
        and attaches with the email response for applicant. Once the file has 
        successfully delivered to applicant, file get deleted from the service.

        Raises error if any of the required  contents are incorrect 
        or missing.
        """
        try:
            data = ApplicationData.from_json(json_data)
            application_content_file = f"app/notification/application_submission/files/{data.application_id}.txt"  # noqa

            with open(
                application_content_file,
                "rb",
            ) as file:

                response = notifications_client.send_email_notification(
                    email_address=data.contact_info,
                    template_id=APPLICATION_RECORD_TEMPLATE_ID,
                    personalisation={
                        "name of fund": data.fund_name,
                        "application id": data.application_id,
                        "date submitted": data.submission_date,
                        "round name": data.fund_round,
                        "question": prepare_upload(file),
                    },
                )
                return response

        except (TypeError, KeyError, AttributeError):
            example_data = json.dumps(get_example_data(), indent=2)
            raise NotificationError(
                message=(
                    "Incorrect data, please check the contents of the"
                    f" notification data.\n\n Example data: {example_data}"
                )
            )

        finally:
            if os.path.exists(application_content_file):
                os.remove(application_content_file)
            else:
                print("The file does not exist")

    @staticmethod
    def send_notification(json_data):
        pass

    @staticmethod
    def send_reminder(json_data):
        pass

    @staticmethod
    def send_award(json_data):
        pass
