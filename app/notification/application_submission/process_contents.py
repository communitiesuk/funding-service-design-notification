from dataclasses import dataclass
from datetime import datetime
from io import StringIO

from app.notification.models.notification import NotificationData


@dataclass
class ApplicationData:
    """Class process the application data to map with
    APPLICATION_RECORD_OF_SUBMISSION template  from
    govuk-notify service.

    Returns:
        Mapped data object from application contents with
        govuk-notify service template & creates txt file
        for applicant to download.
    """

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
    def from_json(data):
        """Function calls ApplicationData class to map
        the application contents.

        Args:
            data: Takes application data from NotificationData
            class.

        Returns:
            ApplicationData object with application contents.
        """
        json_data = NotificationData.notification_data(data)
        application = json_data.content["application"]
        return ApplicationData(
            contact_info=json_data.contact_info,
            questions=ApplicationData.create_memory_object(json_data),
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
        sections = ApplicationData.get_sections(data)
        for section in sections:
            section_names.append(section.get("section_name"))
        return list(dict.fromkeys(section_names))

    @staticmethod
    def get_questions_answers(data) -> dict:
        question_answers = {}
        sections = ApplicationData.get_sections(data)
        section_names = ApplicationData.get_section_names(data)

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
    def create_memory_object(data):
        """Function creates a memory object for question & answers."""
        json_file = ApplicationData.get_questions_answers(data)
        output = StringIO()
        for question, answer in json_file.items():
            output.write(f"- {question}: ")
            output.write(f"{answer}\n")

        return output.getvalue()
