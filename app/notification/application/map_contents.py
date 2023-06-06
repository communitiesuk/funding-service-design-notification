from __future__ import annotations

import collections
import uuid
from dataclasses import dataclass
from datetime import datetime
from io import BytesIO
from io import StringIO
from typing import TYPE_CHECKING

import pytz
from app.notification.model.multi_input_data import MultiInput
from app.notification.model.notification_utils import format_answer
from app.notification.model.notification_utils import simplify_title
from app.notification.notification_contents_base_class import (
    _NotificationContents,
)
from bs4 import BeautifulSoup
from config import Config
from flask import current_app
from fsd_utils.config.notify_constants import NotifyConstants

if TYPE_CHECKING:
    from app.notification.model.notification import Notification


@dataclass
class Application(_NotificationContents):
    contact_info: str
    questions: bytes
    fund_name: str
    fund_id: str
    round_name: str
    reference: str
    reply_to_email_id: str
    submission_date: str = None

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
        current_app.logger.info(
            f"Mapping contents for {notification.template_type}"
        )
        application_data = notification.content[
            NotifyConstants.APPLICATION_FIELD
        ]
        return cls(
            contact_info=notification.contact_info,
            questions=cls.bytes_object_for_questions_answers(notification),
            submission_date=application_data.get("date_submitted"),
            fund_name=application_data.get("fund_name"),
            fund_id=application_data.get("fund_id"),
            round_name=application_data.get("round_name"),
            reference=application_data.get("reference"),
            reply_to_email_id=Config.REPLY_TO_EMAILS_WITH_NOTIFY_ID[
                notification.content.get(
                    NotifyConstants.MAGIC_LINK_CONTACT_HELP_EMAIL_FIELD
                )
            ],
        )

    @classmethod
    def get_forms(cls, notification: Notification) -> list:
        forms = notification.content[NotifyConstants.APPLICATION_FIELD][
            NotifyConstants.APPLICATION_FORMS_FIELD
        ]
        return forms

    @classmethod
    def get_form_names(cls, notification: Notification) -> list:
        form_names = []
        forms = cls.get_forms(notification)
        for form in forms:
            form_names.append(form.get(NotifyConstants.APPLICATION_NAME_FIELD))
        return list(dict.fromkeys(form_names))

    @classmethod
    def get_questions_and_answers(cls, notification: Notification) -> dict:
        """
        Extracts questions and answers from form data.

        Args:
            notification (Notification): The form data containing the questions and answers.

        Returns:
            dict: A dictionary mapping form names to their respective questions and answers.
        """
        questions_answers = collections.defaultdict(dict)
        forms = cls.get_forms(notification)
        form_names = cls.get_form_names(notification)

        for form_name in form_names:
            for form in forms:
                if form_name in form[NotifyConstants.APPLICATION_NAME_FIELD]:
                    for question in form[
                        NotifyConstants.APPLICATION_QUESTIONS_FIELD
                    ]:
                        for field in question["fields"]:
                            answer = field.get("answer")
                            clean_html_answer = cls.remove_html_tags(answer)

                            if field["type"] == "file":
                                # we check if the question type is "file"
                                # then we remove the aws
                                # key attached to the answer

                                if isinstance(clean_html_answer, str):
                                    questions_answers[form_name][
                                        field["title"]
                                    ] = clean_html_answer.split("/")[-1]
                                else:
                                    questions_answers[form_name][
                                        field["title"]
                                    ] = clean_html_answer
                            elif (
                                isinstance(clean_html_answer, bool)
                                and field["type"] == "list"
                            ):
                                questions_answers[form_name][
                                    field["title"]
                                ] = ("Yes" if clean_html_answer else "No")
                            elif (
                                isinstance(clean_html_answer, list)
                                and field["type"] == "multiInput"
                            ):

                                questions_answers[form_name][
                                    field["title"]
                                ] = cls.map_multi_input_data(clean_html_answer)
                            else:
                                questions_answers[form_name][
                                    field["title"]
                                ] = clean_html_answer
        return questions_answers

    @classmethod
    def get_fund_name(cls, notification):
        metadata = notification.content[NotifyConstants.APPLICATION_FIELD]
        return metadata.get("fund_name")

    @classmethod
    def format_questions_answers_with_stringIO(
        cls,
        notification: Notification,
    ) -> str:
        """Function formats dict of questions/answers
        for readability with StringIO."""
        json_file = cls.get_questions_and_answers(notification)
        output = StringIO()

        output.write(
            f"********* {cls.get_fund_name(notification)} **********\n"
        )  # noqa

        for section_name, values in json_file.items():

            title = simplify_title(section_name, remove_text=["cof", "ns"])

            output.write(f"\n* {' '.join(title).capitalize()}\n\n")
            for questions, answers in values.items():
                output.write(f"  Q) {questions}\n")
                output.write(f"  A) {format_answer(answers)}\n\n")
        return output.getvalue()

    @classmethod
    def bytes_object_for_questions_answers(
        cls,
        notification: Notification,
    ) -> BytesIO:
        """Function creates a memory object for question & answers
        with ByteIO from StringIO.
        """
        stringIO_data = cls.format_questions_answers_with_stringIO(
            notification
        )
        convert_to_bytes = bytes(stringIO_data, "utf-8")
        bytes_object = BytesIO(convert_to_bytes)
        return bytes_object

    @classmethod
    def remove_html_tags(cls, answer):
        """
        Removes HTML tags from the provided answer and returns the cleaned text.

        Args:
            answer (str): The answer containing HTML tags.

        Returns:
            str: The cleaned text with HTML tags removed.
        """

        try:

            if answer is None or isinstance(answer, (bool, list)):
                return answer

            soup = BeautifulSoup(answer, "html.parser")
            indent = " " * 5

            if not soup.find():
                return answer.strip()

            if not (soup.ul or soup.ol):
                # Handle other HTML tags
                cleaned_text = soup.get_text()
                cleaned_text = cleaned_text.replace("\xa0", "")
                return cleaned_text.strip()

            soup_list = soup.ul or soup.ol
            list_items = []
            for index, li in enumerate(soup_list.find_all("li"), start=1):
                separator = "." if soup.ul else f"{index}."
                if li.get_text() == "\xa0":
                    continue

                if index > 1:
                    list_items.append(f"{indent}{separator} {li.get_text()}")
                else:
                    list_items.append(f"{separator} {li.get_text()}")
            return "\n".join(list_items)

        except Exception as e:
            current_app.logger.error(
                f"Error occurred while processing HTML tag: {answer}", e
            )
            return answer

    @classmethod
    def map_multi_input_data(cls, multi_input_data):
        """
        Map the multi-input data to a sorted dictionary and process it.

        Args:
            multi_input_data (list): The list of dictionaries representing the multi-input data.

        Returns:
            str: The processed output as a formatted string.
        """

        key = None
        value = None
        sorted_data = {}
        for item in multi_input_data:
            if len(item) < 2:
                for value in item.values():
                    key = str(uuid.uuid4())
                    sorted_data[key] = value
            else:
                key, *value = item.values()
                sorted_data[key] = value

        output = MultiInput.process_data(sorted_data)
        return "\n".join(output)
