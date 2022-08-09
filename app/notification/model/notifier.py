from app.notification.application.map_contents import (
    Application,
)
from app.notification.magic_link.map_contents import ProcessMagicLinkData
from app.notification.model.notification import Notification
from app.notification.model.response import application_error
from app.notification.model.response import application_key_error
from app.notification.model.response import invalid_data_error
from app.notification.model.response import magic_link_error
from app.notification.model.response import magic_link_key_error
from config import Config
from notifications_python_client import errors
from notifications_python_client import NotificationsAPIClient
from tests.test_application.application_data import (
    expected_application_content,
)
from tests.test_magic_link.magic_link_data import expected_magic_link_content

notifications_client = NotificationsAPIClient(Config.GOV_NOTIFY_API_KEY)


class Notifier:
    """Class holds notification operations"""

    @staticmethod
    def send_magic_link(json_data: dict, code: int = 200) -> tuple:
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
            response = (
                notifications_client.send_email_notification(
                    email_address=data.contact_info,
                    template_id=Config.MAGIC_LINK_TEMPLATE_ID,
                    personalisation={
                        "name of fund": data.content["fund_name"],
                        "link to application": data.content["magic_link_url"],
                        "contact details": (
                            "dummy_contact_info@funding-service-help.com"
                        ),
                    },
                ),
                code,
            )
            return response, code
        except errors.HTTPError:
            data = Notification.from_json(process_json_data)
            return invalid_data_error(
                magic_link_error(
                    data.contact_info,
                    data.content.get("fund_name"),
                    data.content.get("magic_link_url"),
                )
            )
        except KeyError:
            return magic_link_key_error(expected_magic_link_content)

    @staticmethod
    def send_application(json_data: dict, code: int = 200) -> tuple:
        """Function maps data eg. questions/answers along with other
        expected contents to the user as expected by the
        govuk-notify-service template.

        Raises error if any of the required  contents are incorrect
        or missing.
        """
        try:
            data = Application.from_json(json_data)
            response = (
                notifications_client.send_email_notification(
                    email_address=data.contact_info,
                    template_id=Config.APPLICATION_RECORD_TEMPLATE_ID,
                    personalisation={
                        "name of fund": data.fund_name,
                        "application id": data.application_id,
                        "date submitted": data.format_submission_date,
                        "round name": data.fund_round,
                        "question": data.questions,
                    },
                ),
                code,
            )
            return response, code

        except errors.HTTPError:
            data = Application.from_json(json_data)
            return invalid_data_error(
                application_error(
                    data.contact_info,
                    data.fund_name,
                    data.application_id,
                    data.format_submission_date,
                    data.fund_round,
                    data.questions,
                )
            )
        except KeyError:
            return application_key_error(expected_application_content)

    @staticmethod
    def send_notification(json_data):
        pass

    @staticmethod
    def send_reminder(json_data):
        pass

    @staticmethod
    def send_award(json_data):
        pass
