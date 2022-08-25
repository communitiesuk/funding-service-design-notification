from dataclasses import dataclass
from datetime import datetime
from io import StringIO

from app.notification.model.notification import Notification


@dataclass
class Application:
    contact_info: str
    questions: dict
    submission_date: str
    fund_name: dict
    fund_round: dict
    application_id: dict

    @property
    def format_submission_date(self):
        if self.submission_date is not None:
            return datetime.strptime(
                self.submission_date, "%Y-%m-%d %H:%M:%S"
            ).strftime("%Y-%m-%d")

    @staticmethod
    def from_json(json_data: dict):
        """Function calls ApplicationData class to map
        the application contents.

        Args:
            data: Takes incoming json_data & converts into class object
            from Notification.from_json

        Returns:
            ApplicationData object with application contents.
        """
        data = Notification.from_json(json_data)
        application = data.content["application"]
        return Application(
            contact_info=data.contact_info,
            questions=Application.process_questions_and_answers(data),
            submission_date=application.get("date_submitted"),
            fund_name=application.get("project_name"),
            fund_round=application.get("round_id"),
            application_id=application.get("id"),
        )

    @staticmethod
    def get_forms(data) -> list:
        forms = data.content["application"]["forms"]
        return forms

    @staticmethod
    def get_form_names(data) -> list:
        form_names = []
        forms = Application.get_forms(data)
        for form in forms:
            form_names.append(form.get("form_name"))
        return list(dict.fromkeys(form_names))

    @staticmethod
    def get_questions_and_answers(data) -> dict:
        question_answers = {}
        forms = Application.get_forms(data)
        form_names = Application.get_form_names(data)

        for form_name in form_names:
            for form in forms:
                if form_name in form["form_name"]:
                    for question in form["questions"]:
                        for fields in question["fields"]:
                            question_answers[fields["title"]] = fields.get(
                                "answer"
                            )
        return question_answers

    @staticmethod
    def process_questions_and_answers(data) -> str:
        """Function creates a memory object for question & answers."""
        json_file = Application.get_questions_and_answers(data)
        output = StringIO()
        for question, answer in json_file.items():
            output.write(f"- {question}: ")
            output.write(f"{answer}\n")
        return output.getvalue()
