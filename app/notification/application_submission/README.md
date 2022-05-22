# funding-service-design-notification-hub

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Code style : black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Repo for the funding service design notification.

Built with Flask.

## Follow main README.md to install & run flask app. 
path: FUNDING-SERVICE-DESIGN-NOTIFICATION/README.md

## How to post data for APPLICATION_RECORD_OF_SUBMISSION.
To post data, use /send endpoint with POST method. Data must be in the following format.

{
    "type": "APPLICATION_RECORD_OF_SUBMISSION",
    "to": "ramandeep.sharma@communities.gov.uk",
    "content": {
        "application":{
            "id": "4c11e4ba-680a-4d06-a862-c241bec77ec4",
            "account_id": "string",
            "status": "NOT_STARTED",
            "fund_id": "fund-a",
            "round_id": "summer",
            "project_name": "Funding service",
            "date_submitted": "21/05/2022",
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
                            "answer": "Harry"
                        },
                        {
                            "key": "applicant-email",
                            "title": "Email",
                            "type": "text",
                            "answer": ""
                        },
                        {
                            "key": "applicant-telephone-number",
                            "title": "Telephone number",
                            "type": "text",
                            "answer": ""
                        },
                        {
                            "key": "applicant-website",
                            "title": "Website",
                            "type": "text",
                            "answer": ""
                        }
                        ],
                        "category": null,
                        "index": null
                    },
                    {
                        "question": "Organisation information",
                        "status": "NOT STARTED",
                        "fields": [
                        {
                            "key": "organisation-name",
                            "title": "Organisation name",
                            "type": "text",
                            "answer": ""
                        },
                        {
                            "key": "organisation-address",
                            "title": "Organisation address",
                            "type": "text",
                            "answer": ""
                        },
                        {
                            "key": "type-of-organisation",
                            "title": "Type of organisation",
                            "type": "list",
                            "answer": ""
                        },
                        {
                            "key": "delivered-projects-like-this-before",
                            "title": "Have you delivered projects like this before?",
                            "type": "list",
                            "answer": ""
                        }
                        ],
                        "category": null,
                        "index": null
                    },
                    {
                        "question": "Responsible people",
                        "status": "NOT STARTED",
                        "fields": [
                        {
                            "key": "organisation-accountant",
                            "title": "Your accountant",
                            "type": "text",
                            "answer": ""
                        },
                        {
                            "key": "responsible-person",
                            "title": "Responsible person",
                            "type": "text",
                            "answer": ""
                        },
                        {
                            "key": "SpLmlI",
                            "title": "Do you have endorsements for this ",
                            "type": "list",
                            "answer": ""
                        },
                        {
                            "key": "organisation-do-you-have-endorsements",
                            "title": "Do you have endorsements to support your application?",
                            "type": "list",
                            "answer": ""
                        },
                        {
                            "key": "who-is-endorsing-your-application",
                            "title": "Who is endorsing your application?",
                            "type": "list",
                            "answer": ""
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
