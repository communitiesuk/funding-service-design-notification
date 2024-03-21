from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from io import BytesIO
from typing import TYPE_CHECKING

import pytz
from flask import current_app
from fsd_utils import extract_questions_and_answers
from fsd_utils import generate_text_of_application
from fsd_utils.config.notify_constants import NotifyConstants

from app.notification.notification_contents_base_class import _NotificationContents
from config import Config

if TYPE_CHECKING:
    from app.notification.model.notification import Notification


@dataclass
class Application(_NotificationContents):
    questions: BytesIO
    fund_id: str
    round_name: str
    reference: str
    reply_to_email_id: str
    submission_date: str = None
    caveats: str = None
    language: str = None

    @property
    def format_submission_date(self):
        if self.submission_date is not None:
            UTC_timezone = pytz.timezone("UTC")
            UK_timezone = pytz.timezone("Europe/London")
            UK_datetime = UTC_timezone.localize(
                datetime.strptime(self.submission_date, "%Y-%m-%dT%H:%M:%S.%f")
            ).astimezone(UK_timezone)

            return (
                UK_datetime.strftime(f"{'%d %B %Y'} at {'%I:%M%p'}")
                .replace("AM", "am")
                .replace("PM", "pm")
            )

    @classmethod
    def from_notification(cls, notification: Notification):
        """Function calls Application class to map
        application contents.

        Args:
            data: Takes an instance of Notification class.

        Returns:
            Application object containing application contents.
        """
        current_app.logger.info(f"Mapping contents for {notification.template_type}")
        application_data = notification.content[NotifyConstants.APPLICATION_FIELD]
        caveats = notification.content.get(NotifyConstants.APPLICATION_CAVEATS, None)
        return cls(
            contact_info=notification.contact_info,
            contact_name=notification.contact_name,
            questions=cls.bytes_object_for_questions_answers(notification),
            submission_date=application_data.get("date_submitted"),
            fund_name=application_data.get("fund_name"),
            fund_id=application_data.get("fund_id"),
            round_name=application_data.get("round_name"),
            reference=application_data.get("reference"),
            language=application_data.get("language"),
            reply_to_email_id=Config.REPLY_TO_EMAILS_WITH_NOTIFY_ID[
                notification.content.get(
                    NotifyConstants.MAGIC_LINK_CONTACT_HELP_EMAIL_FIELD
                )
            ],
            caveats=caveats,
        )

    @classmethod
    def get_forms(cls, notification: Notification) -> list:
        forms = notification.content[NotifyConstants.APPLICATION_FIELD][
            NotifyConstants.APPLICATION_FORMS_FIELD
        ]
        return forms

    @classmethod
    def get_questions_and_answers(cls, notification: Notification) -> dict:
        """
        Extracts questions and answers from form data.

        Args:
            notification (Notification): The form data containing the questions and answers.

        Returns:
            dict: A dictionary mapping form names to their respective questions and answers.
        """
        forms = cls.get_forms(notification)

        questions_answers = extract_questions_and_answers(
            forms, notification.content["application"]["language"]
        )
        return questions_answers

    @classmethod
    def get_fund_name(cls, notification):
        metadata = notification.content[NotifyConstants.APPLICATION_FIELD]
        fund_name = metadata.get("fund_name")
        return (
            f"{fund_name} {round_name}"
            if (round_name := metadata.get("round_name"))
            else fund_name
        )

    @classmethod
    def bytes_object_for_questions_answers(
        cls,
        notification: Notification,
    ) -> BytesIO:
        """Function creates a memory object for question & answers
        with ByteIO from StringIO.
        """
        q_and_a = cls.get_questions_and_answers(notification)
        fund_name = cls.get_fund_name(notification)
        language = notification.content["application"]["language"]
        stringIO_data = generate_text_of_application(
            q_and_a, fund_name, language
        )
        convert_to_bytes = bytes(stringIO_data, "utf-8")
        bytes_object = BytesIO(convert_to_bytes)
        return bytes_object
