import logging
import os
from pathlib import Path

from fsd_utils import CommonConfig
from fsd_utils import NotifyConstants
from fsd_utils import configclass


@configclass
class DefaultConfig:
    FUND_NAME = "Digital Planning Improvement Fund"  # TODO This should not be hard coded

    FLASK_ENV = CommonConfig.FLASK_ENV
    SECRET_KEY = CommonConfig.SECRET_KEY
    SESSION_COOKIE_NAME = os.environ.get("SESSION_COOKIE_NAME")
    FLASK_ROOT = str(Path(__file__).parent.parent.parent)

    GOV_NOTIFY_API_KEY = os.environ.get("GOV_NOTIFY_API_KEY", "gov_notify_api_key")

    MAGIC_LINK_TEMPLATE_ID = os.environ.get("MAGIC_LINK_TEMPLATE_ID", "02a6d48a-f227-4b9a-9dd7-9e0cf203c8a2")

    EXPRESSION_OF_INTEREST_TEMPLATE_ID = {
        "54c11ec2-0b16-46bb-80d2-f210e47a8791": {
            NotifyConstants.TEMPLATE_TYPE_EOI_PASS: {
                "fund_name": "COF",
                "template_id": {
                    "en": "04db42f4-a74e-4ab3-b9e2-565592fd6f46",
                    "cy": "46915152-ee11-4bce-a0e1-ce1033078640",
                },
            },
            NotifyConstants.TEMPLATE_TYPE_EOI_PASS_W_CAVEATS: {
                "fund_name": "COF",
                "template_id": {
                    "en": "705684c7-6985-4d4c-9170-08a85f47b8e1",
                    "cy": "ead6bfc2-f3a1-468c-8d5a-87a32bf31311",
                },
            },
        },
    }

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
        "1e4bd8b0-b399-466d-bbd1-572171bbc7bd": {
            "fund_name": "HSRA",
            "template_id": "52decdde-e796-4b16-a1a0-5f56c9a61b0f",
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
        "1e4bd8b0-b399-466d-bbd1-572171bbc7bd": {
            "fund_name": "HSRA",
            "template_id": "b577de1a-7242-4f9b-b823-6d4f50ad5f19",
        },
    }

    APPLICATION_DEADLINE_REMINDER_TEMPLATE_ID = os.environ.get(
        "APPLICATION_DEADLINE_REMINDER_TEMPLATE_ID",
        "e41cc73d-6947-4cbb-aedd-4ab2f470a2d2",
    )

    ASSESSMENT_APPLICATION_ASSIGNED = os.environ.get(
        "ASSESSMENT_APPLICATION_ASSIGNED", "d4bdc13e-93b4-48ba-8d22-71bf4f480128"
    )

    ASSESSMENT_APPLICATION_UNASSIGNED = os.environ.get(
        "ASSESSMENT_APPLICATION_UNASSIGNED", "9cfaa46c-f122-4532-a9f6-b3c773de6555"
    )

    # Logging
    FSD_LOG_LEVEL = logging.WARNING

    # E.G. "EMAIL": "GOV_NOTIFY_ID"
    REPLY_TO_EMAILS_WITH_NOTIFY_ID = {
        "COF@communities.gov.uk": "10668b8d-9472-4ce8-ae07-4fcc7bf93a9d",
        "transformationfund@levellingup.gov.uk": "25286d9a-8543-41b5-a00f-331b999e51f0",
        "cyprfund@levellingup.gov.uk": "72bb79a8-2748-4404-9f01-14690bee3843",
        "digitalplanningteam@levellingup.gov.uk": "73eecbb1-5dbc-4653-8c58-46aa79151210",
        "HighStreetRentalAuctions@levellingup.gov.uk": "0874cafb-a297-4f3c-bb3f-99bc578cce4a",
    }

    # ---------------
    # Task Executor Config
    # ---------------
    TASK_EXECUTOR_MAX_THREAD = int(os.environ.get("TASK_EXECUTOR_MAX_THREAD", 5))  # max amount of threads
    # ---------------
    # AWS Overall Config
    # ---------------
    AWS_ACCESS_KEY_ID = AWS_SQS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = AWS_SQS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = AWS_SQS_REGION = os.environ.get("AWS_REGION")
    AWS_ENDPOINT_OVERRIDE = os.environ.get("AWS_ENDPOINT_OVERRIDE")

    # ---------------
    # S3 Config
    # ---------------
    AWS_MSG_BUCKET_NAME = os.environ.get("AWS_MSG_BUCKET_NAME")

    # ---------------
    # SQS Config
    # ---------------
    SQS_WAIT_TIME = int(os.environ.get("SQS_WAIT_TIME", 2))  # max time to wait (in sec) before returning
    SQS_BATCH_SIZE = int(os.environ.get("SQS_BATCH_SIZE", 10))  # MaxNumber Of Messages to process
    SQS_VISIBILITY_TIME = int(
        os.environ.get("SQS_VISIBILITY_TIME", 1)
    )  # time for message to temporarily invisible to others (in sec)
    SQS_RECEIVE_MESSAGE_CYCLE_TIME = int(
        os.environ.get("SQS_RECEIVE_MESSAGE_CYCLE_TIME", 5)
    )  # Run the job every 'x' seconds
    AWS_SQS_NOTIF_APP_PRIMARY_QUEUE_URL = os.environ.get("AWS_SQS_NOTIF_APP_PRIMARY_QUEUE_URL")
    AWS_SQS_NOTIF_APP_SECONDARY_QUEUE_URL = os.environ.get("AWS_SQS_NOTIF_APP_SECONDARY_QUEUE_URL")
