import collections
from dataclasses import dataclass
from datetime import datetime
from io import BytesIO
from io import StringIO

from flask import current_app
from fsd_utils.config.notify_constants import NotifyConstants


@dataclass
class Application:
    contact_info: str
    questions: dict
    submission_date: str
    fund_name: str
    fund_round: str
    reference: str

    @property
    def format_submission_date(self):
        if self.submission_date is not None:
            return datetime.strptime(
                self.submission_date, "%Y-%m-%dT%H:%M:%S.%f"
            ).strftime("%Y-%m-%d")

    @staticmethod
    def from_json(data):
        """Function calls ApplicationData class to map
        the application contents.

        Args:
            data: Takes incoming json_data & converts into class object
            from Notification.from_json

        Returns:
            ApplicationData object with application contents.
        """
        current_app.logger.info(f"Mapping contents for {data.template_type}")
        application = data.content[NotifyConstants.APPLICATION_FIELD]
        return Application(
            contact_info=data.contact_info,
            questions=Application.bytes_object_for_questions_answers(data),
            submission_date=application.get("date_submitted"),
            fund_name=application.get("project_name"),
            fund_round=application.get("round_name"),
            reference=application.get("id"),
        )

    @staticmethod
    def get_forms(data) -> list:
        forms = data.content[NotifyConstants.APPLICATION_FIELD][
            NotifyConstants.APPLICATION_FORMS_FIELD
        ]
        return forms

    @staticmethod
    def get_form_names(data) -> list:
        form_names = []
        forms = Application.get_forms(data)
        for form in forms:
            form_names.append(form.get(NotifyConstants.APPLICATION_NAME_FIELD))
        return list(dict.fromkeys(form_names))

    @staticmethod
    def get_questions_and_answers(data) -> dict:
        """function grabs all the forms & checks the question type "file"
        is None or bool the returns None or boolean value.
        If not, then removes the attached database from the file answer.

        returns: dict of questions & answers from all forms.
        """
        question_answers = collections.defaultdict(dict)
        forms = Application.get_forms(data)
        form_names = Application.get_form_names(data)

        for form_name in form_names:
            for form in forms:
                if form_name in form[NotifyConstants.APPLICATION_NAME_FIELD]:
                    for question in form[
                        NotifyConstants.APPLICATION_QUESTIONS_FIELD
                    ]:
                        for fields in question["fields"]:
                            if fields["type"] == "file":
                                answer = fields.get("answer")
                                if (
                                    answer is not None
                                    and type(answer) is not bool
                                ):

                                    question_answers[form_name][
                                        fields["title"]
                                    ] = answer.split("/")[-1]
                                else:
                                    question_answers[form_name][
                                        fields["title"]
                                    ] = fields.get("answer")

                            else:
                                question_answers[form_name][
                                    fields["title"]
                                ] = fields.get("answer")
        return question_answers

    @staticmethod
    def format_questions_answers_with_stringIO(data) -> str:
        """Function formats the data for readability with StringIO."""
        application = data.content[NotifyConstants.APPLICATION_FIELD]
        json_file = Application.get_questions_and_answers(data)
        output = StringIO()

        output.write(f"{application.get('project_name')}\n")
        for form_name, values in json_file.items():
            output.write(f"\n- {form_name}\n")
            for questions, answers in values.items():
                output.write(f" . {questions}: ")
                output.write(f"{answers}\n")
        return output.getvalue()

    @staticmethod
    def bytes_object_for_questions_answers(data) -> BytesIO:
        """Function creates a memory object for question & answers
        with ByteIO from StringIO.
        """
        stringIO_data = Application.format_questions_answers_with_stringIO(
            data
        )
        convert_to_bytes = bytes(stringIO_data, "utf-8")
        bytes_object = BytesIO(convert_to_bytes)
        return bytes_object
