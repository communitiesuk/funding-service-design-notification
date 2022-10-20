# funding-service-design-notification-hub

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Code style : black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Repo for the funding service design notification.

Built with Flask.

## Follow main README.md to install & run flask app

path: FUNDING-SERVICE-DESIGN-NOTIFICATION/README.md

## How to post data for template APPLICATION_DEADLINE_REMINDER

To post data, use /send endpoint with POST method. Data must be in the following format.

    {
        "type": "APPLICATION_DEADLINE_REMINDER",
        "to": "email@example.com",
        "content": {
            "application": {
            "round_name": "WINDOW 2 ROUND 2",
            "reference":"WUHJFDWJ",
            "deadline_date":"2022-05-20 14:47:12"
            }
        }
    }
