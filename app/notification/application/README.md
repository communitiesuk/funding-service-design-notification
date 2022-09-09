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
        "to": "testing_application@example.com",
        "content": {
            "application": {
            "id": "5176687c-3c5a-44f5-8580-fa6e552bfb3e",
            "round_id": "summer",
            "project_name": "Funding service community fund",
            "date_submitted": "2022-05-20T14:47:12.111511",
            "forms": [
                {
                "name": "community-benefits",
                "questions": [
                    {
                    "question": "Potential to deliver community benefits",
                    "fields": [
                        {
                        "title": "Question one",
                        "answer": "Answer one"
                        }
                    ]
                    }
                ]
                },
                {
                "name": "declarations",
                "questions": [
                    {
                    "question": "Declarations",
                    "fields": [
                        {
                        "title": "Question two",
                        "answer": [
                            "Answer two (item one)",
                            "Answer two (item two)"
                        ]
                        }
                    ]
                    }
                ]
                }
            ]
            }
        }
    }
