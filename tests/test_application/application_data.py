expected_application_content = "Key content must contain Application data that is expected to deliver to the user & data must be in the JSON format"

expected_application_data = {
    "type": "APPLICATION_RECORD_OF_SUBMISSION",
    "to": "example_email@test.com",
    "content": {
        "application": {
            "id": "123456789",
            "account_id": "string",
            "status": "NOT_STARTED",
            "fund_id": "fund-a",
            "round_id": "summer",
            "project_name": "Funding service",
            "date_submitted": "2022-05-14 10:20:44",
            "started_at": "2022-05-20 14:47:12",
            "last_edited": None,
            "sections": [
                {
                    "section_name": "about-your-org",
                    "status": "NOT_STARTED",
                    "questions": [
                        {
                            "question": "Application information",
                            "status": "NOT STARTED",
                            "fields": [
                                {
                                    "key": "application-name",
                                    "title": "Applicant name",
                                    "type": "text",
                                    "answer": "Jack-Simon",
                                },
                            ],
                            "category": None,
                            "index": None,
                        }
                    ],
                    "metadata": {"paymentSkipped": None},
                }
            ],
        }
    },
}


unexpected_application_data = {
    "type": "APPLICATION_RECORD_OF_SUBMISSION",
    "to": "example_email@test.com",
    "content": {},
}


expected_application_response = {
    "notify_response": {
        "content": {
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
