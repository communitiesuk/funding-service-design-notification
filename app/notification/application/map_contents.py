from __future__ import annotations

import collections
from dataclasses import dataclass
from datetime import datetime
from io import BytesIO
from io import StringIO
from typing import TYPE_CHECKING

import pytz
from config import Config
from flask import current_app
from fsd_utils.config.notify_constants import NotifyConstants

if TYPE_CHECKING:
    from app.notification.model.notification import Notification

from bs4 import BeautifulSoup  # noqa E402


@dataclass
class Application:
    contact_info: str
    questions: bytes
    fund_name: str
    round_name: str
    reference: str
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
            fund_name=Config.FUND_NAME,
            round_name=application_data.get("round_name"),
            reference=application_data.get("reference"),
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
                                ] = cls.sort_multi_input_data(
                                    clean_html_answer
                                )
                            else:
                                questions_answers[form_name][
                                    field["title"]
                                ] = clean_html_answer
        return questions_answers

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
            "*********"
            f" {Config.FUND_NAME}{' ' + ' '.join(list(json_file.keys())[0].split('cof', 1)[-1][1:].upper().split('-')).strip() if 'cof' in list(json_file.keys())[0] else ''} **********\n"  # noqa
        )

        for section_name, values in json_file.items():
            title = (
                [
                    item
                    for item in section_name.split("-")[
                        : section_name.split("-").index("cof")
                    ]
                    if "cof" not in item
                ]
                if "cof" in section_name.split("-")
                else section_name.split("-")
            )

            output.write(f"\n* {' '.join(title).capitalize()}\n\n")
            for questions, answers in values.items():
                output.write(f"  Q) {questions}\n")
                output.write(f"  A) {answers}\n\n")
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

        Example with unordered lis (ul) tags:
        answer = '<ul><li>Item 1</li><li>Item 2</li></ul>'
        cleaned_text = remove_html_tags(cls, answer)
        print(cleaned_text)
        # Output:
        #     - Item 1
        #     - Item 2

        Example with ordered list (ol) tags:
        answer = '<ol><li>First item</li><li>Second item</li></ol>'
        cleaned_text = remove_html_tags(cls, answer)
        print(cleaned_text)
        # Output:
        #     1. First item
        #     2. Second item
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
                separator = "-" if soup.ul else f"{index}."
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
    def sort_multi_input_data(cls, multi_input_data):
        """
        Sorts and formats multi-input data.

        Args:
            multi_input_data (list[dict]): A list of dictionaries representing multi-input data.
            example: [{'GLQlOh': 'cost one', 'JtwkMy': 4444}, {'GLQl6y': 'cost two', 'JtwkMt': 4455}]

        Returns:
            str: A formatted string representation of the sorted multi-input data.
            example: A) - cost one: £4444
                        - cost two: £4455
        """
        key = None
        value = None
        sorted_data = {}
        indent = " " * 5

        for items in multi_input_data:
            key, value = items.values()

            sorted_data[key] = value

        return "\n".join(
            [
                f"{indent}- {key.strip()}: £{value}"
                if index != 1
                else f"- {key.strip()}: £{value}"
                for index, (key, value) in enumerate(
                    sorted_data.items(), start=1
                )
            ]
        )
