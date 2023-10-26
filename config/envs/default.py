import json
import logging
import os
from pathlib import Path

from fsd_utils import configclass


@configclass
class DefaultConfig:

    FUND_NAME = "Community Ownership Fund"

    SECRET_KEY = os.environ.get("SECRET_KEY")
    SESSION_COOKIE_NAME = os.environ.get("SESSION_COOKIE_NAME")
    FLASK_ROOT = str(Path(__file__).parent.parent.parent)
    FLASK_ENV = os.environ.get("FLASK_ENV")

    GOV_NOTIFY_API_KEY = os.environ.get(
        "GOV_NOTIFY_API_KEY", "gov_notify_api_key"
    )

    MAGIC_LINK_TEMPLATE_ID = os.environ.get(
        "MAGIC_LINK_TEMPLATE_ID", "02a6d48a-f227-4b9a-9dd7-9e0cf203c8a2"
    )

    APPLICATION_RECORD_TEMPLATE_ID = {
        "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4": {
            "fund_name": "COF",
            "template_id": "0ddadcb3-ebe7-44f9-90e6-80ff3b61e0cb",
        },
        "13b95669-ed98-4840-8652-d6b7a19964db": {
            "fund_name": "NSTF",
            "template_id": "487c62f1-9aeb-4cc2-b996-5bdf0d02854b",
        },
        "1baa0f68-4e0a-4b02-9dfe-b5646f089e65": {
            "fund_name": "CYP",
            "template_id": "1c69f104-edfa-49d7-9bab-cbbd30c323f3",
        },
        "f493d512-5eb4-11ee-8c99-0242ac120002": {
            "fund_name": "DPI",
            "template_id": "6e1d80ac-c843-4b47-9946-ecad542dd5de",
        },
    }

    INCOMPLETE_APPLICATION_TEMPLATE_ID = {
        "47aef2f5-3fcb-4d45-acb5-f0152b5f03c4": {
            "fund_name": "COF",
            "template_id": "fc8cff7c-a595-4590-a1a4-eccda48d8604",
        },
        "13b95669-ed98-4840-8652-d6b7a19964db": {
            "fund_name": "NSTF",
            "template_id": "d4c9cb6f-c36d-4157-a5e4-0b7bc323e332",
        },
        "1baa0f68-4e0a-4b02-9dfe-b5646f089e65": {
            "fund_name": "CYP",
            "template_id": "5e308d1e-4d1d-4572-9c99-9a8396224aed",
        },
        "f493d512-5eb4-11ee-8c99-0242ac120002": {
            "fund_name": "DPI",
            "template_id": "7980eee3-5a40-42b8-98dc-ba3b11ea4e65",
        },
    }

    APPLICATION_DEADLINE_REMINDER_TEMPLATE_ID = os.environ.get(
        "APPLICATION_DEADLINE_REMINDER_TEMPLATE_ID",
        "e41cc73d-6947-4cbb-aedd-4ab2f470a2d2",
    )

    # Logging
    FSD_LOG_LEVEL = logging.WARNING

    # E.G. "EMAIL": "GOV_NOTIFY_ID"
    REPLY_TO_EMAILS_WITH_NOTIFY_ID = {
        "COF@levellingup.gov.uk": "10668b8d-9472-4ce8-ae07-4fcc7bf93a9d",
        "transformationfund@levellingup.gov.uk": (
            "25286d9a-8543-41b5-a00f-331b999e51f0"
        ),
        "cyprfund@levellingup.gov.uk": "72bb79a8-2748-4404-9f01-14690bee3843",
        "digitalplanningteam@levellingup.gov.uk": (
            "73eecbb1-5dbc-4653-8c58-46aa79151210"
        ),
    }

    if "PRIMARY_QUEUE_URL" in os.environ:
        AWS_REGION = os.environ.get("AWS_REGION")
        AWS_PRIMARY_QUEUE_URL = os.environ.get("PRIMARY_QUEUE_URL")
        AWS_SECONDARY_QUEUE_URL = os.environ.get("DEAD_LETTER_QUEUE_URL")
    elif "VCAP_SERVICES" in os.environ:
        vcap_services = json.loads(os.environ["VCAP_SERVICES"])
        if "aws-sqs-queue" in vcap_services:
            sqs_credentials = vcap_services["aws-sqs-queue"][0]["credentials"]
            AWS_REGION = sqs_credentials["aws_region"]
            AWS_ACCESS_KEY_ID = sqs_credentials["aws_access_key_id"]
            AWS_SECRET_ACCESS_KEY = sqs_credentials["aws_secret_access_key"]
            AWS_PRIMARY_QUEUE_URL = sqs_credentials["primary_queue_url"]
            AWS_SECONDARY_QUEUE_URL = sqs_credentials["secondary_queue_url"]
    else:
        AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
        AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
        AWS_REGION = os.environ.get("AWS_REGION")
        AWS_PRIMARY_QUEUE_URL = ""
        AWS_SECONDARY_QUEUE_URL = ""
    AWS_DLQ_ASSESSMENT_IMPORT_MAX_RECIEVE_COUNT = int(
        os.environ.get("AWS_DLQ_ASSESSMENT_IMPORT_MAX_RECIEVE_COUNT", 3)
    )

    # ---------------
    # SQS Config
    # ---------------
    SQS_WAIT_TIME = int(
        os.environ.get("SQS_WAIT_TIME", 2)
    )  # max time to wait (in sec) before returning
    SQS_BATCH_SIZE = int(
        os.environ.get("SQS_BATCH_SIZE", 1)
    )  # MaxNumber Of Messages to process
    SQS_VISIBILITY_TIME = int(
        os.environ.get("SQS_VISIBILITY_TIME", 1)
    )  # time for message to temporarily invisible to others (in sec)
    SQS_RECEIVE_MESSAGE_CYCLE_TIME = int(
        os.environ.get("SQS_RECEIVE_MESSAGE_CYCLE_TIME", 60)
    )  # Run the job every 'x' seconds

