from app.notification.model.notification import Notification
from fsd_utils.config.notify_constants import NotifyConstants


expected_application_json = {
    NotifyConstants.FIELD_TYPE: NotifyConstants.TEMPLATE_TYPE_APPLICATION,
    NotifyConstants.FIELD_TO: "test_application@example.com",
    NotifyConstants.FIELD_CONTENT: {
        NotifyConstants.MAGIC_LINK_CONTACT_HELP_EMAIL_FIELD: (
            "COF@levellingup.gov.uk"
        ),
        NotifyConstants.APPLICATION_FIELD: {
            "id": "123456789",
            "reference": "1564564564-56-4-54-4654",
            "fund_id": "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4",
            "round_name": "summer",
            "date_submitted": "2022-05-14T09:25:44.124542",
            "fund_name": "Community Ownership Fund",
            "language": "en",
            NotifyConstants.APPLICATION_FORMS_FIELD: [
                {
                    NotifyConstants.APPLICATION_NAME_FIELD: "about-your-org",
                    NotifyConstants.APPLICATION_QUESTIONS_FIELD: [
                        {
                            "question": "Application information",
                            "fields": [
                                {
                                    "key": "application-name",
                                    "title": "Applicant name",
                                    "type": "text",
                                    "answer": "Jack-Simon",
                                },
                                {
                                    "key": "upload-file",
                                    "title": "Upload file",
                                    "type": "file",
                                    "answer": "012ba4c7-e4971/test-one_two.three/programmer.jpeg",  # noqa
                                },
                                {
                                    "key": "boolean-question-1",
                                    "title": "Boolean Question 1 ",
                                    "type": "list",
                                    "answer": False,
                                },
                                {
                                    "key": "boolean-question-2",
                                    "title": "Boolean Question 2",
                                    "type": "list",
                                    "answer": True,
                                },
                            ],
                        }
                    ],
                }
            ],
        },
    },
}

expected_application_json_with_none_answers = {
    NotifyConstants.FIELD_TYPE: NotifyConstants.TEMPLATE_TYPE_APPLICATION,
    NotifyConstants.FIELD_TO: "test_application@example.com",
    NotifyConstants.FIELD_CONTENT: {
        NotifyConstants.MAGIC_LINK_CONTACT_HELP_EMAIL_FIELD: (
            "COF@levellingup.gov.uk"
        ),
        NotifyConstants.APPLICATION_FIELD: {
            "id": "123456789",
            "reference": "1564564564-56-4-54-4654",
            "fund_id": "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4",
            "round_name": "summer",
            "date_submitted": "2022-05-14T14:25:44.124542",
            "fund_name": "Community Ownership Fund",
            NotifyConstants.APPLICATION_FORMS_FIELD: [
                {
                    NotifyConstants.APPLICATION_NAME_FIELD: "about-your-org",
                    NotifyConstants.APPLICATION_QUESTIONS_FIELD: [
                        {
                            "question": "Application information",
                            "fields": [
                                {
                                    "key": "application-name",
                                    "title": "Applicant name",
                                    "type": "text",
                                    "answer": None,
                                },
                                {
                                    "key": "upload-file",
                                    "title": "Upload file",
                                    "type": "file",
                                    "answer": None,  # noqa
                                },
                            ],
                        }
                    ],
                }
            ],
        },
    },
}


expected_application_reminder_json = {
    NotifyConstants.FIELD_TYPE: "APPLICATION_DEADLINE_REMINDER",
    NotifyConstants.FIELD_TO: "test_application_reminder@example.com",
    NotifyConstants.FIELD_CONTENT: {
        NotifyConstants.APPLICATION_FIELD: {
            "round_name": "WINDOW 2 ROUND 2",
            "reference": "WUHJFDWJ",
            "deadline_date": "2022-05-20T14:47:12",
            "contact_help_email": "COF@levellingup.gov.uk",
        }
    },
}

unexpected_application_json = {
    NotifyConstants.FIELD_TYPE: NotifyConstants.TEMPLATE_TYPE_APPLICATION,
    NotifyConstants.FIELD_TO: "example_email@test.com",
    NotifyConstants.FIELD_CONTENT: {},
}


expected_application_response = (
    {
        "content": {
            "body": (
                "#Fund name - Night Shelter Transformation Fund"
                " \r\n---\r\nApplication id: 7bc21539 \r\n---\r\nDate"
                " submitted: 2023-08-04\r\n---     \r\nRound name: Round"
                " 2\r\n---\r\n"
            ),
            "from_email": "sender@service.gov.uk",
        },
    },
)

expected_eoi_application_response = (
    {
        "content": {
            "body": (
                "#Fund name - Expression Of Interest"
                " \r\n---\r\nApplication id: 7bc21539 \r\n---\r\nDate"
                " submitted: 2023-08-04\r\n---     \r\nRound name: Round"
                " 2\r\n---\r\n"
            ),
            "from_email": "sender@service.gov.uk",
        },
    },
)


def notification_class_data_for_application(
    date_submitted=True, deadline_date=True, language="en"
):
    return Notification(
        template_type="APPLICATION_RECORD_OF_SUBMISSION",
        contact_info="sender@service.gov.uk",
        contact_name="Test User",
        content={
            "application": {
                "language": language,
                "reference": "NSTF",
                "id": "7bc21539",
                "status": "SUBMITTED",
                "last_edited": "2023-08-04T15:47:21.274900",
                "started_at": "2023-08-04T15:47:21.274900",
                "deadline_date": "2023-12-12T15:47:21"
                if deadline_date
                else None,
                "round_name": "Round 2",
                "forms": [
                    {
                        "name": "current-services-ns",
                        "status": "NOT_STARTED",
                        "questions": [],
                    },
                ],
                "date_submitted": "2023-08-04T15:47:23.208849"
                if date_submitted
                else None,
                "account_id": "6802f603",
                "fund_id": "13b95669-ed98-4840-8652-d6b7a19964db",
                "project_name": None,
                "round_id": "fc7aa604",
                "fund_name": "Night Shelter Transformation Fund",
            },
            "contact_help_email": "transformationfund@levellingup.gov.uk",
        },
    )


def notification_class_data_for_eoi(
    date_submitted=True, deadline_date=True, language="en"
):
    return Notification(
        template_type="APPLICATION_RECORD_OF_SUBMISSION",
        contact_info="sender@service.gov.uk",
        contact_name="Test User",
        content={
            "application": {
                "language": language,
                "reference": "EOI",
                "id": "7bc21539",
                "status": "SUBMITTED",
                "last_edited": "2023-08-04T15:47:21.274900",
                "started_at": "2023-08-04T15:47:21.274900",
                "deadline_date": "2023-12-12T15:47:21"
                if deadline_date
                else None,
                "round_name": "Round 2",
                "forms": [
                    {
                        "name": "current-services-ns",
                        "status": "NOT_STARTED",
                        "questions": [],
                    },
                ],
                "date_submitted": "2023-08-04T15:47:23.208849"
                if date_submitted
                else None,
                "account_id": "6802f603",
                "fund_id": "54c11ec2-0b16-46bb-80d2-f210e47a8791",
                "project_name": None,
                "round_id": "fc7aa604",
                "fund_name": "Expression Of Interest",
            },
            "contact_help_email": "transformationfund@levellingup.gov.uk",
            "caveats": [
                "Stop cutting trees to be eligible for applying for the fund"
            ],
        },
    )
