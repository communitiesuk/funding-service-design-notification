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
        }
    },
}

expected_application_data_contains_none_answers = {
    NotifyConstants.FIELD_TYPE: NotifyConstants.TEMPLATE_TYPE_APPLICATION,
    NotifyConstants.FIELD_TO: "test_application@example.com",
    NotifyConstants.FIELD_CONTENT: {
        NotifyConstants.APPLICATION_FIELD: {
            "id": "123456789",
            "reference": "1564564564-56-4-54-4654",
            "fund_id": "fund-a",
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
        }
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


multi_input_test_data = {
    "process_data": {
        "multiple_values": {
            "input_data": {
                "trusts one": [
                    125,
                    "1 April 2023 to 31 March 2024",
                    "Capital",
                    True,
                ],
                "trust two": [
                    456,
                    "1 April 2024 to 31 March 2025",
                    "Revenue",
                    False,
                ],
            },
            "expected_response": [
                ". trusts one: [125, '1 April 2023 to 31 March 2024',"
                " 'Capital', 'Yes']",
                "     . trust two: [456, '1 April 2024 to 31 March 2025',"
                " 'Revenue', 'No']",
            ],
        },
        "single_value": {
            "input_data": {
                "bbd0ec2a-972f-4d06-bf93-bf24786c3859": "Sky builders",
                "ac8bbdfe-6a39-45b8-8c0a-6558148388d1": "trust builders",
            },
            "expected_response": [". Sky builders", "     . trust builders"],
        },
        "iso_values": {
            "input_data": {
                "Project one": [{"PrulfI__month": 1, "PrulfI__year": 2021}],
                "Project two": [{"PrulfI__month": 2, "PrulfI__year": 2022}],
            },
            "expected_response": (
                [
                    ". Project one: ['month: 1', 'year: 2021']",
                    "     . Project two: ['month: 2', 'year: 2022']",
                ]
            ),
        },
    },
    "map_data": {
        "multiple_values": {
            "input_data": [
                {
                    "AfAKxk": "trusts one",
                    "CrcLtW": 125,
                    "ndySbC": "1 April 2023 to 31 March 2024",
                    "pATWyM": "Capital",
                    "sIFBGc": True,
                },
                {
                    "AfAKxk": "trust two",
                    "CrcLtW": 456,
                    "ndySbC": "1 April 2024 to 31 March 2025",
                    "pATWyM": "Revenue",
                    "sIFBGc": False,
                },
            ],
            "expected_response": (
                ". trusts one: [125, '1 April 2023 to 31 March 2024',"
                " 'Capital', 'Yes']\n     . trust two: [456, '1 April 2024 to"
                " 31 March 2025', 'Revenue', 'No']"
            ),
        },
        "single_value": {
            "input_data": [
                {"CZZYvE": "Sky builders"},
                {"CZZYvE": "trust builders"},
            ],
            "expected_response": ". Sky builders\n     . trust builders",
        },
        "integer_values": {
            "input_data": [
                {"GLQlOh": "cost one", "JtwkMy": 4444},
                {"GLQl6y": "cost two", "JtwkMt": 4455},
            ],
            "expected_response": ". cost one: 4444\n     . cost two: 4455",
        },
    },
}
