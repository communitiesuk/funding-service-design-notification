# funding-service-design-notification-hub

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Code style : black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Repo for the funding service design notification.

Built with Flask.

## Follow main README.md to install & run flask app

path: FUNDING-SERVICE-DESIGN-NOTIFICATION/README.md

## How to post data for APPLICATION_RECORD_OF_SUBMISSION

To post data, use /send endpoint with POST method. Data must be in the following format.

    {
    "type": "APPLICATION_RECORD_OF_SUBMISSION",
    "to": "example_email@test.com",
    "content": {
        "application":{
            "id": "123456789-jack",
            "account_id": "string",
            "status": "NOT_STARTED",
            "fund_id": "fund-a",
            "round_id": "summer",
            "project_name": "Funding service",
            "date_submitted": "2022-05-14 10:20:44",
            "started_at": "2022-05-20 14:47:12",
            "last_edited": null,
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
                            "answer": "Jack Simon"
                        },
                        {
                            "key": "applicant-email",
                            "title": "Email",
                            "type": "text",
                            "answer": "test@example.com"
                        },
                        {
                            "key": "applicant-telephone-number",
                            "title": "Telephone number",
                            "type": "text",
                            "answer": "012345678"
                        },
                        {
                            "key": "applicant-website",
                            "title": "Website",
                            "type": "text",
                            "answer": "www.example.com"
                        }
                        ],
                        "category": null,
                        "index": null
                    }
                    ],
                    "metadata": {
                    "paymentSkipped": null
                    }
                }
                ]
            }}}
