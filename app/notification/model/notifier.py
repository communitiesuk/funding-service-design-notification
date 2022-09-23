from app.notification.application.map_contents import Application
from app.notification.magic_link.map_contents import MagicLink
from app.notification.model.response import invalid_data_error
from config import Config
from flask import current_app
from notifications_python_client import errors
from notifications_python_client import NotificationsAPIClient
from notifications_python_client import prepare_upload


notifications_client = NotificationsAPIClient(Config.GOV_NOTIFY_API_KEY)


class Notifier:
    """Class holds notification operations"""

    @staticmethod
    def send_magic_link(json_data: dict, code: int = 200) -> tuple:
        """Function maps data eg. magic link along with other
        expected contents to the user as expected by the
        govuk-notify-service template.

        Raises HTTPError if any of the required  contents are incorrect
        or missing.
        """
        try:
            data = MagicLink.from_json(json_data)
            response = notifications_client.send_email_notification(
                email_address=data.contact_info,
                template_id=Config.MAGIC_LINK_TEMPLATE_ID,
                personalisation={
                    "name of fund": data.fund_name,
                    "link to application": data.magic_link,
                    "request new link url": data.request_new_link_url,
                    "contact details": data.contact_help_email,
                },
            )
            current_app.logger.info("Call made to govuk Notify API")
            return response, code
        except errors.HTTPError:
            current_app.logger.exception(
                "HTTPError while sending notification"
            )
            return invalid_data_error(MagicLink.from_json(json_data))

    @staticmethod
    def send_application(json_data: dict, code: int = 200) -> tuple:
        """Function maps data eg. questions/answers along with other
        expected contents to the user as expected by the
        govuk-notify-service template.

        Raises HTTPError if any of the required contents are incorrect
        or missing.
        """
        try:
            data = Application.from_json(json_data)
            response = notifications_client.send_email_notification(
                email_address=data.contact_info,
                template_id=Config.APPLICATION_RECORD_TEMPLATE_ID,
                personalisation={
                    "name of fund": data.fund_name,
                    "application reference": data.application_id,
                    "date submitted": data.format_submission_date,
                    "round name": data.fund_round,
                    "question": prepare_upload(data.questions),
                },
            )
            current_app.logger.info("Call made to govuk Notify API")
            return response, code

        except errors.HTTPError:
            current_app.logger.exception(
                "HTTPError while sending notification"
            )
            return invalid_data_error(Application.from_json(json_data))

    @staticmethod
    def send_notification(json_data):
        pass

    @staticmethod
    def send_reminder(json_data):
        pass

    @staticmethod
    def send_award(json_data):
        pass
