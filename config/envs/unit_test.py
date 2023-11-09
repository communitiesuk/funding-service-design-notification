import logging

from config.envs.default import DefaultConfig
from fsd_utils import configclass


@configclass
class UnitTestConfig(DefaultConfig):
    #  Application Config
    SECRET_KEY = "dev"  # pragma: allowlist secret
    SESSION_COOKIE_NAME = "session_cookie"

    # Logging
    FSD_LOG_LEVEL = logging.DEBUG

    REPLY_TO_EMAILS_WITH_NOTIFY_ID = {
        "nope@wrong.gov.uk": "100",
        "COF@levellingup.gov.uk": "10668b8d-9472-4ce8-ae07-4fcc7bf93a9d",
        "transformationfund@levellingup.gov.uk": (
            "25286d9a-8543-41b5-a00f-331b999e51f0"
        ),
    }
