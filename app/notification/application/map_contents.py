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
    def get_sections(data) -> list:
        sections = data.content["application"]["sections"]
        return sections

    @staticmethod
    def get_section_names(data) -> list:
        section_names = []
        sections = Application.get_sections(data)
        for section in sections:
            section_names.append(section.get("section_name"))
        return list(dict.fromkeys(section_names))

    @staticmethod
    def get_questions_and_answers(data) -> dict:
        question_answers = {}
        sections = Application.get_sections(data)
        section_names = Application.get_section_names(data)

        for section_name in section_names:
            for section in sections:
                if section_name in section["section_name"]:
                    for question in section["questions"]:
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
