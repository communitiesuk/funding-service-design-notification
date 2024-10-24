from __future__ import annotations

from typing import TYPE_CHECKING

from flask import current_app
from notifications_python_client import NotificationsAPIClient
from notifications_python_client import errors

from app.notification.application.map_contents import Application
from app.notification.application_reminder.map_contents import ApplicationReminder
from app.notification.assessment.map_contents import Assignment
from app.notification.magic_link.map_contents import MagicLink
from app.notification.model.response import invalid_data_error
from config import Config

if TYPE_CHECKING:
    from app.notification.model.notification import Notification


class Notifier:
    """Class holds notification operations"""

    @staticmethod
    def send_magic_link(notification: Notification, code: int = 200) -> tuple:
        """Function makes a call to govuk-notify-service with mapped contents
        that are expected by the govuk-notify-service template.

        Args: Takes an instance of Notification class.

        Raises HTTPError if any of the required contents are incorrect
        or missing.

        """
        try:
            notifications_client = NotificationsAPIClient(Config.GOV_NOTIFY_API_KEY)
            contents = MagicLink.from_notification(notification)
            current_app.logger.info(
                f"Getting template for fund id [{contents.fund_id}] and template id {Config.MAGIC_LINK_TEMPLATE_ID}")
            response = notifications_client.send_email_notification(
                email_address=contents.contact_info,
                template_id=Config.MAGIC_LINK_TEMPLATE_ID,
                email_reply_to_id=contents.reply_to_email_id,
                personalisation={
                    "name of fund": contents.fund_name,
                    "link to application": contents.magic_link,
                    "request new link url": contents.request_new_link_url,
                    "contact details": contents.contact_help_email,
                },
            )
            current_app.logger.info("Call made to govuk Notify API")
            return response, code
        except errors.HTTPError:
            current_app.logger.exception("HTTPError while sending notification")
            return invalid_data_error(MagicLink.from_notification(notification))

    @staticmethod
    def send_submitted_application(notification: Notification, code: int = 200) -> tuple:
        """Function makes a call to govuk-notify-service with mapped contents
        that are expected by the govuk-notify-service template.

        Args: Takes an instance of Notification class.

        Raises HTTPError if any of the required contents are incorrect
        or missing.
        """
        try:
            notifications_client = NotificationsAPIClient(Config.GOV_NOTIFY_API_KEY)
            contents = Application.from_notification(notification)
            current_app.logger.info(
                f"Getting template for fund id [{contents.fund_id}] and template id {Config.APPLICATION_RECORD_TEMPLATE_ID[contents.fund_id]['template_id']}")
            response = notifications_client.send_email_notification(
                email_address=contents.contact_info,
                template_id=Config.APPLICATION_RECORD_TEMPLATE_ID[contents.fund_id]["template_id"].get(
                    contents.language, "en"
                ),
                email_reply_to_id=contents.reply_to_email_id,
                personalisation={
                    "name of fund": contents.fund_name,
                    "application reference": contents.reference,
                    "date submitted": contents.format_submission_date,
                    "round name": contents.round_name,
                    "question": {
                        "file": contents.questions,
                        "filename": None,
                        "confirm_email_before_download": None,
                        "retention_period": None,
                    },
                },
            )
            current_app.logger.info("Call made to govuk Notify API")
            return response, code

        except errors.HTTPError:
            current_app.logger.exception("HTTPError while sending notification")
            return invalid_data_error(Application.from_notification(notification))

    @staticmethod
    def send_submitted_eoi(notification: Notification, code: int = 200, template_name: str = "") -> tuple:
        """Function makes a call to govuk-notify-service with mapped contents
        that are expected by the govuk-notify-service template.

        Args: Takes an instance of Notification class.

        Raises HTTPError if any of the required contents are incorrect
        or missing.
        """
        try:
            notifications_client = NotificationsAPIClient(Config.GOV_NOTIFY_API_KEY)
            contents = Application.from_notification(notification)
            current_app.logger.info(
                f"Getting template for fund id [{contents.fund_id}] and template id {Config.EXPRESSION_OF_INTEREST_TEMPLATE_ID[contents.fund_id][template_name]['template_id']}")
            response = notifications_client.send_email_notification(
                email_address=contents.contact_info,
                template_id=Config.EXPRESSION_OF_INTEREST_TEMPLATE_ID[contents.fund_id][template_name][
                    "template_id"
                ].get(contents.language, "en"),
                email_reply_to_id=contents.reply_to_email_id,
                personalisation={
                    "name of fund": contents.fund_name,
                    "application reference": contents.reference,
                    "date submitted": contents.format_submission_date,
                    "round name": contents.round_name,
                    "question": {
                        "file": contents.questions,
                        "filename": None,
                        "confirm_email_before_download": None,
                        "retention_period": None,
                    },
                    "caveats": contents.caveats,
                    "full name": contents.contact_name,
                },
            )
            current_app.logger.info("Call made to govuk Notify API")
            return response, code

        except errors.HTTPError:
            current_app.logger.exception("HTTPError while sending notification")
            return invalid_data_error(Application.from_notification(notification))

    @staticmethod
    def send_incomplete_application(notification: Notification, code: int = 200) -> tuple:
        """Function makes a call to govuk-notify-service with mapped contents
        that are expected by the govuk-notify-service template.

        Args: Takes an instance of Notification class.

        Raises HTTPError if any of the required contents are incorrect
        or missing.
        """
        try:
            notifications_client = NotificationsAPIClient(Config.GOV_NOTIFY_API_KEY)
            contents = Application.from_notification(notification)
            current_app.logger.info(
                f"Getting template for fund id [{contents.fund_id}] and template id {Config.INCOMPLETE_APPLICATION_TEMPLATE_ID[contents.fund_id]['template_id']}")
            response = notifications_client.send_email_notification(
                email_address=contents.contact_info,
                email_reply_to_id=contents.reply_to_email_id,
                template_id=Config.INCOMPLETE_APPLICATION_TEMPLATE_ID[contents.fund_id]["template_id"],
                personalisation={
                    "name of fund": contents.fund_name,
                    "application reference": contents.reference,
                    "round name": contents.round_name,
                    "question": {
                        "file": contents.questions,
                        "filename": None,
                        "confirm_email_before_download": None,
                        "retention_period": None,
                    },
                },
            )
            current_app.logger.info("Call made to govuk Notify API")
            return response, code

        except errors.HTTPError:
            current_app.logger.exception("HTTPError while sending notification")
            return invalid_data_error(Application.from_notification(notification))

    @staticmethod
    def send_application_reminder(notification: Notification, code: int = 200) -> tuple:
        """Function makes a call to govuk-notify-service with mapped contents
        that are expected by the govuk-notify-service template.

        Args: Takes an instance of Notification class.

        Raises HTTPError if any of the required contents are incorrect
        or missing.
        """
        try:
            notifications_client = NotificationsAPIClient(Config.GOV_NOTIFY_API_KEY)
            contents = ApplicationReminder.from_notification(notification)
            current_app.logger.info(
                f"Getting template for fund id [{contents.fund_id}] and template id {Config.APPLICATION_DEADLINE_REMINDER_TEMPLATE_ID}")
            response = notifications_client.send_email_notification(
                email_address=contents.contact_info,
                template_id=Config.APPLICATION_DEADLINE_REMINDER_TEMPLATE_ID,
                email_reply_to_id=contents.reply_to_email_id,
                personalisation={
                    "name of fund": contents.fund_name,
                    "application reference": contents.reference,
                    "round name": contents.round_name,
                    "application deadline": contents.deadline_date,
                },
            )
            current_app.logger.info("Call made to govuk Notify API")
            return response, code

        except errors.HTTPError:
            current_app.logger.exception("HTTPError while sending notification")
            return invalid_data_error(Application.from_notification(notification))

    @staticmethod
    def send_assessment_assigned(notification: Notification, code: int = 200) -> tuple:
        try:
            notifications_client = NotificationsAPIClient(Config.GOV_NOTIFY_API_KEY)
            contents = Assignment.from_notification(notification)
            current_app.logger.info(
                f"Getting template for fund id [{contents.fund_id}] and template id {Config.ASSESSMENT_APPLICATION_ASSIGNED}")
            # Note that this uses the default Notify account reply-to unless we specify otherwise
            response = notifications_client.send_email_notification(
                email_address=contents.contact_info,
                template_id=Config.ASSESSMENT_APPLICATION_ASSIGNED,
                personalisation={
                    "fund_name": contents.fund_name,
                    "reference_number": contents.reference_number,
                    "project_name": contents.project_name,
                    "assignment message": ("Message: " + contents.message) if contents.message else "",
                    "assessment link": contents.assessment_link,
                    "lead assessor email": contents.lead_assessor_email,
                },
            )
            current_app.logger.info("Call made to govuk Notify API")
            return response, code

        except errors.HTTPError:
            current_app.logger.exception("HTTPError while sending notification")
            return invalid_data_error(Assignment.from_notification(notification))

    @staticmethod
    def send_assessment_unassigned(notification: Notification, code: int = 200) -> tuple:
        try:
            notifications_client = NotificationsAPIClient(Config.GOV_NOTIFY_API_KEY)
            contents = Assignment.from_notification(notification)
            current_app.logger.info(
                f"Getting template for fund id [{contents.fund_id}] and template id {Config.ASSESSMENT_APPLICATION_UNASSIGNED}")
            # Note that this uses the default Notify account reply-to unless we specify otherwise
            response = notifications_client.send_email_notification(
                email_address=contents.contact_info,
                template_id=Config.ASSESSMENT_APPLICATION_UNASSIGNED,
                personalisation={
                    "fund_name": contents.fund_name,
                    "reference_number": contents.reference_number,
                    "project_name": contents.project_name,
                    "assignment message": ("Message: " + contents.message) if contents.message else "",
                    "assessment link": contents.assessment_link,
                    "lead assessor email": contents.lead_assessor_email,
                },
            )
            current_app.logger.info("Call made to govuk Notify API")
            return response, code

        except errors.HTTPError:
            current_app.logger.exception("HTTPError while sending notification")
            return invalid_data_error(Assignment.from_notification(notification))
