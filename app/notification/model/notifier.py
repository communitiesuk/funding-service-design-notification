from app.notification.application.map_contents import (
    Application,
)
from app.notification.magic_link.map_contents import ProcessMagicLinkData
from app.notification.model.exceptions import NotificationError
from app.notification.model.notification import Notification
from config import Config
from notifications_python_client import NotificationsAPIClient
from examplar_data.application_data import (
    expected_application_data,
)
from examplar_data.magic_link_data import (
    expected_magic_link_data,
)

notifications_client = NotificationsAPIClient(Config.GOV_NOTIFY_API_KEY)


class Notifier:
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
            data = Notification.from_json(process_json_data)
            response = notifications_client.send_email_notification(
                email_address=data.contact_info,
                template_id=Config.MAGIC_LINK_TEMPLATE_ID,
                personalisation={
                    "name of fund": data.content["fund_name"],
                    "link to application": data.content["magic_link_url"],
                    "contact details": (
                        "dummy_contact_info@funding-service-help.com"
                    ),
                },
            )
            return response
        except:  # noqa
            raise NotificationError(
                message=(
                    "Incorrect MAGIC LINK data, please check the contents of"
                    " the MAGIC LINK data. \nExample data:"
                    f" {expected_magic_link_data}"
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
            data = Application.from_json(json_data)
            response = notifications_client.send_email_notification(
                email_address=data.contact_info,
                template_id=Config.APPLICATION_RECORD_TEMPLATE_ID,
                personalisation={
                    "name of fund": data.fund_name,
                    "application id": data.application_id,
                    "date submitted": data.format_submission_date,
                    "round name": data.fund_round,
                    "question": data.questions,
                },
            )
            return response

        except:  # noqa
            raise NotificationError(
                message=(
                    "Incorrect APPLICATION data, please check the contents of"
                    " the APPLICATION data. \nExample data:"
                    f" {expected_application_data}"
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
