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
Refer to the steps as required
### Create a new notification api key
api key is required for a service to communicate with GOV.UK Notify service

- Refer to the link [here](https://www.notifications.service.gov.uk/services/505ca282-bfde-4fae-8d8a-ff09906a23fa/api/keys) to create a new api key as required

### Add api key to the notification service
Production api key <span style="color:red">**(DO NOT USE IT LOCALLY)**</span>
 - The production api key must always be kept secure hence it is added to the Github secrets.

Test api key <span style="color:lightgreen">**(for local use)**</span>
- The test api key can be temporarily added to the config file or export it to the local environment for testing purposes only. Make sure to remove the test api key from config file before committing any changes.
 Set it as an environment variable e.g.
    ```
    // pragma: allowlist secret
    export GOV_NOTIFY_API_KEY="api-key-value
    ```
    Note: For unit (integration) testing, you also need to set this in `pytest.ini`

### Create a new template
Template is required for a service to communicate with GOV.UK Notify service.

Typically, a template contains information in a text format, with attributes enclosed in double parentheses, such as ((attribute name)). These attribute will then be required for a service to make a call to that unique template.

- Refer to the link [here](https://www.notifications.service.gov.uk/services/505ca282-bfde-4fae-8d8a-ff09906a23fa/templates) to create a new template

### Add new template in the notification service
Once a template is created using the GOV.UK Notify service, it generates a unique template ID. This ID can then be directly incorporated into the configuration file. Then this template ID can be used across the service and to make a call to the GOV.UK Notify service.

- For example APPLICATION_RECORD_TEMPLATE_ID is added [here](https://github.com/communitiesuk/funding-service-design-notification/blob/17d27ed6b7bba556214a01d1196d828b583ab40d/config/envs/default.py#L30)

### Format contents for readability (optional)
When an applicant submits their application, we send a file containing the application's questions and answers back to the applicant and at the end of the assessment, once the QA section is completed, we make files available for download containing the application's questions and answers. There is a functionality within the utils-service [here](https://github.com/communitiesuk/funding-service-design-utils/blob/af29613c764e83b1690d4cb25ca21341113b20af/fsd_utils/mapping/application/qa_mapping.py#L13), which is employed by both the notification service and assessment frontend to facilitate this task.

To ensure that questions and answers are mapped correctly and formatted for better readability, especially when creating a new fund, it's essential to review the questions & answers. The text file can be located in [GOV.UK Notify service](https://www.notifications.service.gov.uk/services/505ca282-bfde-4fae-8d8a-ff09906a23fa/api) after the application submission.

<span style="color:yellow">The dev team recently carried out some work to organise and arrange the questions and answers, making it easier for all services to use them. The notification service may not require the mapping and formatting, so instead, the formatting can happen in the application-store. Then, the notification service can simply act as a dumb service to send messages to users without needing to do extra organising.</span>

### Post contents to GOV.UK Notify service
Instantiate a notifications_client object using the notification api key. Next, utilise the preferred service, like send_email_notification, to access the email service.

For this service (notifications_client.send_email_notification), you'll need to some required attributes such as email_address, template_id, email_reply_to_id etc.

Based on the attributes set on the template during its creation, ensure that all attribute values are added to personalisation.

- To connect with GOV.UK Notify service  and post contents, refer to this [example](https://github.com/communitiesuk/funding-service-design-notification/blob/17d27ed6b7bba556214a01d1196d828b583ab40d/app/notification/model/notifier.py#L25).

**For more information, refer to the documentation** [here](https://www.notifications.service.gov.uk/using-notify).

### Configuring new fund on Notification service
- Refer to the documentation [here](https://dluhcdigital.atlassian.net/wiki/spaces/FS/pages/45973632/Configuring+Notification+service+for+New+Funds+and+Templates)


### To run the service locally

    `flask run`

Note: This service is an internal service so it doesn't have the frontend.

# Run with Gunicorn

In deployed environments the service is run with gunicorn. You can run the service locally with gunicorn to test

First set the FLASK_ENV environment you wish to test eg:

    export FLASK_ENV=dev

Then run gunicorn using the following command:

    gunicorn wsgi:app -c run/gunicorn/local.py


### Build with Paketo

[Pack](https://buildpacks.io/docs/tools/pack/cli/pack_build/)

[Paketo buildpacks](https://paketo.io/)

```pack build <name your image> --builder paketobuildpacks/builder:base```

Example:

```
[~/work/repos/funding-service-design-notification] pack build paketo-demofsd-app --builder paketobuildpacks/builder:base
***
Successfully built image paketo-demofsd-app
```

You can then use that image with docker to run a container

```
docker run -d -p 8080:8080 --env PORT=8080 --env FLASK_ENV=dev [envs] paketo-demofsd-app
```

`envs` needs to include values for each of:
GOV_NOTIFY_API_KEY
SENTRY_DSN
GITHUB_SHA

```
docker ps -a
CONTAINER ID   IMAGE                       COMMAND                  CREATED          STATUS                    PORTS                    NAMES
42633142c619   paketo-demofsd-app          "/cnb/process/web"       8 seconds ago    Up 7 seconds              0.0.0.0:8080->8080/tcp   peaceful_knuth
```

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

## Copilot Initialisation

Copilot is the deployment of the infrastructure configuration, which is all stored under the copilot folder. The manifest files have been pre-generated by running through various initialisation steps that create the manifest files by prompting a series of questions, but do not _deploy_ the infrastructure.

For each AWS account, these commands will need to be run _once_ to initialise the environment:

`copilot app init pre-award` - this links the pre-award app with the current service, and associates the next commands with the service. Essentially, this provides context for the service to run under

```
    copilot init \
    --name fsd-notification \
    --app pre-award \
    --type 'Backend Service' \
    --image 'ghcr.io/communitiesuk/funding-service-design-notification:latest' \
    --port 80
```

This will initalise this service, using the current created image
