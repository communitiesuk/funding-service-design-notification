from config.envs.default import DefaultConfig
from fsd_utils import configclass
import logging


@configclass
class DevelopmentConfig(DefaultConfig):
    #  Application Config
    SECRET_KEY = "dev"
    SESSION_COOKIE_NAME = "session_cookie"
    FLASK_ENV = "development"

    # Logging
    FSD_LOG_LEVEL = logging.DEBUG
