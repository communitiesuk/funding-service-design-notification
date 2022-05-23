from dataclasses import dataclass

from app.notification.models.notification import NotificationData


@dataclass
class ApplicationData:
    """class process the application data to map with
    APPLICATION_RECORD_OF_SUBMISSION template  from
    govuk-notify service.

    Returns:
        Mapped data with govuk-notify service & creates txt file
        for applicant to download the application contents.
    """

    contact_info: str
    questions: dict
    submission_date: str
    fund_name: dict
    fund_round: dict
    application_id: dict

    @staticmethod
    def from_json(data):
        json_data = NotificationData.notification_data(data)
        application = json_data.content["application"]
        return ApplicationData(
            contact_info=json_data.contact_info,
            questions=ApplicationData.create_text_file(json_data),
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
    def create_text_file(data):
        application_id = data.content["application"]
        json_file = ApplicationData.get_questions_answers(data)

        with open(
            f"app/notification/application_submission/files/{application_id['id']}.txt",  # noqa
            "w",
            encoding="utf-8",
        ) as file:
            for question, answer in json_file.items():
                file.write("%s: %s\n" % (question, answer))
