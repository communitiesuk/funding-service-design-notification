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
            "application": {
                "id": "5176687c-3c5a-44f5-8580-fa6e552bfb3e",
                "round_id": "summer",
                "project_name": "Funding service",
                "started_at": "2022-08-18 15:14:14",
                "date_submitted": "2022-05-20 14:47:12",
                "forms": [
                    {
                        "form_name": "community-benefits",
                        "questions": [
                            {
                                "question": "Potential to deliver community benefits",
                                "fields": [
                                    {
                                        "key": "QjJtbs",
                                        "title": "What community benefits do you expect to deliver with this project? ",
                                        "type": "list",
                                        "answer": [
                                            "community-pride",
                                            "JACK"
                                        ]
                                    },
                                    {
                                        "key": "gDTsgG",
                                        "title": "Tell us about these benefits in detail, and explain how you'll measure the benefits it'll bring for the community",
                                        "type": "text",
                                        "answer": "Explaining benefits"
                                    }
                                ],
                                "status": "COMPLETED"
                            }
                        ]
                    },
                    {
                        "form_name": "declarations",
                        "questions": [
                            {
                                "question": "Declarations",
                                "fields": [
                                    {
                                        "key": "LlvhYl",
                                        "title": "Confirm you have considered subsidy control and state aid implications for your project, and the information you have given us is correct",
                                        "type": "list",
                                        "answer": "YESSSSSS"
                                    }
                                ],
                                "status": "COMPLETED"
                            }
                        ]
                    }
                ]
            }
        }
    }
