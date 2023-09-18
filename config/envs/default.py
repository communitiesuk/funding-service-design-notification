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
    }

    INCOMPLETE_APPLICATION_TEMPLATE_ID = os.environ.get(
        "INCOMPLETE_APPLICATION_TEMPLATE_ID",
        "fc8cff7c-a595-4590-a1a4-eccda48d8604",
    )
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
        "cyprfund@levellingup.gov.uk": "205dc7fd-605c-4656-8e93-ed764f6740ef",
    }
