examplar_magic_link_data = {
    "type": "MAGIC_LINK",
    "to": "test_recipient@email.com",
    "content": {
        "magic_link_url": "MAGIC-LINK-GOES-HERE",
        "fund_name": "FUND NAME GOES HERE",
    },
}

examplar_application_data = {
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