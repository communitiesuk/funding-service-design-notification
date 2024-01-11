# funding-service-design-notification-hub

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Code style : black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This repository hosts a Flask web service for a Funding Notification System, specializing in magic link notifications.

[Developer setup guide](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-setup.md)

This service depends on:
-funding-service-design-utils

## How to use
1. Set-up an API KEY that requires to connect with the govuk-notify-service

    Click on the link & follow the instructions to set-up an API KEY.
    https://docs.notifications.service.gov.uk/python.html#api-keys

    Set it as an environment variable e.g.
    ```
    // pragma: allowlist secret
    export GOV_NOTIFY_API_KEY="api-key-value
    ```

    Note: For unit (integration) testing, you also need to set this in `pytest.ini`

2. Enter the virtual environment as described above, then:

    `flask run`

    Note: This service is an internal service so it doesn't have the frontend.

## How to post data for notification service.

Go to relevant service. See example
path: app/notification/magic_link/README.md

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

# Builds and Deploys
Details on how our pipelines work and the release process is available [here](https://dluhcdigital.atlassian.net/wiki/spaces/FS/pages/73695505/How+do+we+deploy+our+code+to+prod)
## Paketo
Paketo is used to build the docker image which gets deployed to our test and production environments. Details available [here](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-paketo.md)
## Copilot
Copilot is used for infrastructure deployment. Instructions are available [here](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-copilot.md), with the following values for the fund store:
- service-name: fsd-fund-store
- image-name: funding-service-design-notification
