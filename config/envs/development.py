import logging

from fsd_utils import configclass

from config.envs.default import DefaultConfig


@configclass
class DevelopmentConfig(DefaultConfig):
    #  Application Config
    SECRET_KEY = "dev"  # pragma: allowlist secret
    SESSION_COOKIE_NAME = "session_cookie"
    FLASK_ENV = "development"

    # Logging
    FSD_LOG_LEVEL = logging.INFO
