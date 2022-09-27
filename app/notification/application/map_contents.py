import collections
from dataclasses import dataclass
from datetime import datetime
from io import BytesIO
from io import StringIO
from typing import TYPE_CHECKING

from flask import current_app
from fsd_utils.config.notify_constants import NotifyConstants

if TYPE_CHECKING:
    from app.notification.model.notification import Notification


@dataclass
class Application:
    contact_info: str
    questions: bytes
    submission_date: str
    fund_name: str
    round_name: str
    reference: str

    @property
    def format_submission_date(self):
        if self.submission_date is not None:
            return datetime.strptime(
                self.submission_date, "%Y-%m-%dT%H:%M:%S.%f"
            ).strftime("%Y-%m-%d")

    @staticmethod
    def from_notification(notification: "Notification"):
        """Function calls ApplicationData class to map
        the application contents.

        Args:
            data: Takes incoming json_data & converts into class object
            from Notification.from_json

        Returns:
            ApplicationData object with application contents.
        """
        current_app.logger.info(
            f"Mapping contents for {notification.template_type}"
        )
        application_data = notification.content[
            NotifyConstants.APPLICATION_FIELD
        ]
        return Application(
            contact_info=notification.contact_info,
            questions=Application.bytes_object_for_questions_answers(
                notification
            ),
            submission_date=application_data.get("date_submitted"),
            fund_name=application_data.get("project_name"),
            round_name=application_data.get("round_name"),
            reference=application_data.get("reference"),
        )

    @staticmethod
    def get_forms(notification: "Notification") -> list:
        forms = notification.content[NotifyConstants.APPLICATION_FIELD][
            NotifyConstants.APPLICATION_FORMS_FIELD
        ]
        return forms

    @staticmethod
    def get_form_names(notification: "Notification") -> list:
        form_names = []
        forms = Application.get_forms(notification)
        for form in forms:
            form_names.append(form.get(NotifyConstants.APPLICATION_NAME_FIELD))
        return list(dict.fromkeys(form_names))

    @staticmethod
    def get_questions_and_answers(notification: "Notification") -> dict:
        """function takes the form data and returns
        dict of questions & answers.
        """
        questions_answers = collections.defaultdict(dict)
        forms = Application.get_forms(notification)
        form_names = Application.get_form_names(notification)

        for form_name in form_names:
            for form in forms:
                if form_name in form[NotifyConstants.APPLICATION_NAME_FIELD]:
                    for question in form[
                        NotifyConstants.APPLICATION_QUESTIONS_FIELD
                    ]:
                        for field in question["fields"]:
                            answer = field.get("answer")
                            if field["type"] == "file":
                                # we check if the question type is "file"
                                # then we remove the aws
                                # key attached to the answer

                                if isinstance(answer, str):
                                    questions_answers[form_name][
                                        field["title"]
                                    ] = answer.split("/")[-1]
                                else:
                                    questions_answers[form_name][
                                        field["title"]
                                    ] = answer

                            else:
                                questions_answers[form_name][
                                    field["title"]
                                ] = answer
        return questions_answers

    @staticmethod
    def format_questions_answers_with_stringIO(
        notification: "Notification",
    ) -> str:
        """Function formats the data for readability with StringIO."""
        application = notification.content[NotifyConstants.APPLICATION_FIELD]
        json_file = Application.get_questions_and_answers(notification)
        output = StringIO()

        output.write(f"{application.get('project_name')}\n")
        for form_name, values in json_file.items():
            output.write(f"\n- {form_name}\n")
            for questions, answers in values.items():
                output.write(f" . {questions}: ")
                output.write(f"{answers}\n")
        return output.getvalue()

    @staticmethod
    def bytes_object_for_questions_answers(
        notification: "Notification",
    ) -> BytesIO:
        """Function creates a memory object for question & answers
        with ByteIO from StringIO.
        """
        stringIO_data = Application.format_questions_answers_with_stringIO(
            notification
        )
        convert_to_bytes = bytes(stringIO_data, "utf-8")
        bytes_object = BytesIO(convert_to_bytes)
        return bytes_object
