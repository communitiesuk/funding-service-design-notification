# funding-service-design-notification-hub

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Code style : black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Repo for the funding service design notification.

Built with Flask.

## Prerequisites

- python ^= 3.10

# Getting started

## Installation

Clone the repository

### Create a Virtual environment

    python3 -m venv .venv

### Enter the virtual environment

...either macOS using bash:

    source .venv/bin/activate

...or if on Windows using Command Prompt:

    .venv\Scripts\activate.bat

### Install dependencies
From the top-level directory enter the command to install pip and the dependencies of the project

    python3 -m pip install --upgrade pip && pip install -r requirements-dev.txt

NOTE: requirements-dev.txt and requirements.txt are updated using [pip-tools pip-compile](https://github.com/jazzband/pip-tools)
To update requirements please manually add the dependencies in the .in files (not the requirements.txt files)
Then run:

    pip-compile requirements.in

    pip-compile requirements-dev.in

## How to use
1. Set-up an API KEY that requires to connect with the govuk-notify-service

    Click on the link & follow the instructions to set-up an API KEY.
    https://docs.notifications.service.gov.uk/python.html#api-keys

    Set it as an environment variable e.g.
    `export GOV_NOTIFY_API_KEY="api-key-value"`

    Note: For unit (integration) testing, you also need to set this in `pytest.ini`

1. Enter the virtual environment as described above, then:

        flask run

    Note: This service is an internal service so it doesn't have the frontend.

## How to post data for notification service.

Go to relevant service. See example
path: app/notification/magic_link/README.md for


# Pipelines

Place brief descriptions of Pipelines here

- Deploy to Gov PaaS - This is a simple pipeline to demonstrate capabilities.  Builds, tests and deploys a simple python application to the PaaS for evaluation in Dev and Test Only.

# Testing

This repo comes with a `.pre-commit-config.yaml`, if you wish to use this do
the following while in your virtual enviroment:

    pip install pre-commit black

    pre-commit install

Once the above is done you will have autoformatting and pep8 compliance built
into your workflow. You will be notified of any pep8 errors during commits.
