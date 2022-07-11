import logging
import os

from fsd_utils import configclass


@configclass
class DefaultConfig:

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

    # Logging
    FSD_LOG_LEVEL = logging.WARNING
