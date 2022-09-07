import logging
import os
from pathlib import Path

from fsd_utils import CommonConfig
from fsd_utils import configclass


@configclass
class DefaultConfig:

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
    APPLICATION_RECORD_TEMPLATE_ID = os.environ.get(
        "APPLICATION_RECORD_TEMPLATE_ID",
        "0ddadcb3-ebe7-44f9-90e6-80ff3b61e0cb",
    )

    # Magic Link Fields
    NOTIFICATION_MAGIC_LINK_CONTACT_HELP_EMAIL = (
        CommonConfig.NOTIFICATION_MAGIC_LINK_CONTACT_HELP_EMAIL
    )
    NOTIFICATION_MAGIC_LINK_MAGIC_LINK_URL = (
        CommonConfig.NOTIFICATION_MAGIC_LINK_MAGIC_LINK_URL
    )
    NOTIFICATION_MAGIC_LINK_REQUEST_NEW_EMAIL_URL = (
        CommonConfig.NOTIFICATION_MAGIC_LINK_REQUEST_NEW_EMAIL_URL
    )
    NOTIFICATION_MAGIC_LINK_FUND_NAME = (
        CommonConfig.NOTIFICATION_MAGIC_LINK_FUND_NAME
    )

    # Logging
    FSD_LOG_LEVEL = logging.WARNING
