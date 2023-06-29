from fsd_utils.config.notify_constants import NotifyConstants

expected_application_content = (
    "Key 'content' must contain the required Application data & the data must"
    " be in the JSON format"
)

expected_application_data = {
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

expected_application_data_contains_none_answers = {
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


expected_application_reminder_data = {
    NotifyConstants.FIELD_TYPE: "APPLICATION_DEADLINE_REMINDER",
    NotifyConstants.FIELD_TO: "test_application_reminder@example.com",
    NotifyConstants.FIELD_CONTENT: {
        NotifyConstants.APPLICATION_FIELD: {
            "round_name": "WINDOW 2 ROUND 2",
            "reference": "WUHJFDWJ",
            "deadline_date": "2022-05-20 14:47:12",
        }
    },
}

unexpected_application_data = {
    NotifyConstants.FIELD_TYPE: NotifyConstants.TEMPLATE_TYPE_APPLICATION,
    NotifyConstants.FIELD_TO: "example_email@test.com",
    NotifyConstants.FIELD_CONTENT: {},
}


expected_application_response = {
    "notify_response": {
        NotifyConstants.FIELD_CONTENT: {
            "body": (
                "#Fund name - Funding service   \r\n---\r\nApplication id:"
                " 123456789 \r\n---\r\nDate submitted: 2022-05-14\r\n---    "
                " \r\nRound name: summer\r\n---\r\nList of questions & answers"
                " for application Funding service\r\n---\r\n- Applicant name:"
                " Jack-Simon"
            ),
            "from_email": "example_sender@service.gov.uk",
        },
    },
    "status": "ok",
}
