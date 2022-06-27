# funding-service-design-notification-hub

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Code style : black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Repo for the funding service design notification.

Built with Flask.

## Follow main README.md to install & run flask app.

path: FUNDING-SERVICE-DESIGN-NOTIFICATION/README.md

## How to post data for MAGIC_LINK

To post data, use /send endpoint with POST method. Data must be in the following format.

    {
        "type": "MAGIC_LINK",
        "to": "example_email@test.com",
        "content": {
            "magic_link_url": "https://www.example.com/",
            "fund_name": "Funding service",
        },
    }
