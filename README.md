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

    python3 -m pip install --upgrade pip && pip install -r requirements.txt

### Set-up an API KEY that requires to connect with the govuk-notify-service.

    Click on the link & follow the instructions to set-up an API KEY.
    https://docs.notifications.service.gov.uk/python.html#api-keys

## How to use
Enter the virtual environment as described above, then:

    flask run

## How to post data for notification service.

Go to relevant service. See example
path: app/notification/magic_link/README.md for


# Pipelines

Place brief descriptions of Pipelines here

* Deploy to Gov PaaS - This is a simple pipeline to demonstrate capabilities.  Builds, tests and deploys a simple python application to the PaaS for evaluation in Dev and Test Only.

Testing

Unit & Accessibility Testing
To run all tests including aXe accessibility tests (using Chrome driver for Selenium) in a development environment run:

...on macOS

pytest --driver Chrome --driver-path .venv/lib/python3.10/site-packages/chromedriver_py/chromedriver_mac64
...on linux64

pytest --driver Chrome --driver-path .venv/lib/python3.10/site-packages/chromedriver_py/chromedriver_linux64
...on win32

pytest --driver Chrome --driver-path .venv/lib/python3.10/site-packages/chromedriver_py/chromedriver_win32.exe
The aXe reports are printed at /axe_reports

This repo comes with a .pre-commit-config.yaml, if you wish to use this do
the following while in your virtual enviroment:

    pip install pre-commit black

    pre-commit install

Once the above is done you will have autoformatting and pep8 compliance built
into your workflow. You will be notified of any pep8 errors during commits.
