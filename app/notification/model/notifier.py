from __future__ import annotations

from typing import TYPE_CHECKING

from app.notification.application.map_contents import Application
from app.notification.application_reminder.map_contents import (
    ApplicationReminder,
)
from app.notification.magic_link.map_contents import MagicLink
from app.notification.model.response import invalid_data_error
from config import Config
from flask import current_app
from notifications_python_client import errors
from notifications_python_client import NotificationsAPIClient
from notifications_python_client import prepare_upload

if TYPE_CHECKING:
    from app.notification.model.notification import Notification

notifications_client = NotificationsAPIClient(Config.GOV_NOTIFY_API_KEY)


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
            contents = MagicLink.from_notification(notification)
            response = notifications_client.send_email_notification(
                email_address=contents.contact_info,
                template_id=Config.MAGIC_LINK_TEMPLATE_ID,
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
            current_app.logger.exception(
                "HTTPError while sending notification"
            )
            return invalid_data_error(
                MagicLink.from_notification(notification)
            )

    @staticmethod
    def send_submitted_application(
        notification: Notification, code: int = 200
    ) -> tuple:
        """Function makes a call to govuk-notify-service with mapped contents
        that are expected by the govuk-notify-service template.

        Args: Takes an instance of Notification class.

        Raises HTTPError if any of the required contents are incorrect
        or missing.
        """
        try:
            contents = Application.from_notification(notification)
            response = notifications_client.send_email_notification(
                email_address=contents.contact_info,
                template_id=Config.APPLICATION_RECORD_TEMPLATE_ID,
                personalisation={
                    "name of fund": contents.fund_name,
                    "application reference": contents.reference,
                    "date submitted": contents.format_submission_date,
                    "round name": contents.round_name,
                    "question": prepare_upload(contents.questions),
                },
            )
            current_app.logger.info("Call made to govuk Notify API")
            return response, code

        except errors.HTTPError:
            current_app.logger.exception(
                "HTTPError while sending notification"
            )
            return invalid_data_error(
                Application.from_notification(notification)
            )

    @staticmethod
    def send_incomplete_application(
        notification: Notification, code: int = 200
    ) -> tuple:
        """Function makes a call to govuk-notify-service with mapped contents
        that are expected by the govuk-notify-service template.

        Args: Takes an instance of Notification class.

        Raises HTTPError if any of the required contents are incorrect
        or missing.
        """
        try:
            contents = Application.from_notification(notification)

            response = notifications_client.send_email_notification(
                email_address=contents.contact_info,
                template_id=Config.INCOMPLETE_APPLICATION_TEMPLATE_ID,
                personalisation={
                    "name of fund": contents.fund_name,
                    "application reference": contents.reference,
                    "round name": contents.round_name,
                    "question": prepare_upload(contents.questions),
                },
            )
            current_app.logger.info("Call made to govuk Notify API")
            return response, code

        except errors.HTTPError:
            current_app.logger.exception(
                "HTTPError while sending notification"
            )
            return invalid_data_error(
                Application.from_notification(notification)
            )

    @staticmethod
    def send_application_reminder(
        notification: Notification, code: int = 200
    ) -> tuple:
        """Function makes a call to govuk-notify-service with mapped contents
        that are expected by the govuk-notify-service template.

        Args: Takes an instance of Notification class.

        Raises HTTPError if any of the required contents are incorrect
        or missing.
        """
        try:
            contents = ApplicationReminder.from_notification(notification)

            response = notifications_client.send_email_notification(
                email_address=contents.contact_info,
                template_id=Config.APPLICATION_DEADLINE_REMINDER_TEMPLATE_ID,
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
            current_app.logger.exception(
                "HTTPError while sending notification"
            )
            return invalid_data_error(
                Application.from_notification(notification)
            )

    @staticmethod
    def send_award(json_data):
        pass
