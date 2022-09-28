from fsd_utils.config.notify_constants import NotifyConstants

expected_application_content = (
    "Key 'content' must contain the required Application data & the data must"
    " be in the JSON format"
)

expected_application_data = {
    NotifyConstants.FIELD_TYPE: NotifyConstants.TEMPLATE_TYPE_APPLICATION,
    NotifyConstants.FIELD_TO: "test_application@example.com",
    NotifyConstants.FIELD_CONTENT: {
        NotifyConstants.APPLICATION_FIELD: {
            "id": "123456789",
            "reference": "1564564564-56-4-54-4654",
            "fund_id": "fund-a",
            "round_name": "summer",
            "date_submitted": "2022-05-14T10:20:44.124542",
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
                            ],
                        }
                    ],
                }
            ],
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
            "subject": "Record of application Funding service",
        },
        "id": "baa18127-b4ea-4fe3-b904-73da684a1f25",
        "reference": None,
        "scheduled_for": None,
        "template": {
            "id": "0ddadcb3-ebe7-44f9-90e6-80ff3b61e0cb",
            "uri": "https://api.notifications.service.gov.uk/services/505ca282-bfde-4fae-8d8a-ff09906a23fa/templates/0ddadcb3-ebe7-44f9-90e6-80ff3b61e0cb",  # noqa
            "version": 32,
        },
        "uri": "https://api.notifications.service.gov.uk/v2/notifications/baa18127-b4ea-4fe3-b904-73da684a1f25",  # noqa
    },
    "status": "ok",
}
