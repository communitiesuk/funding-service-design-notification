import logging
from config.envs.default import DefaultConfig
from fsd_utils import configclass


@configclass
class UnitTestConfig(DefaultConfig):

    #  Application Config
    SECRET_KEY = "dev"
    SESSION_COOKIE_NAME = "session_cookie"

    # Logging
    FSD_LOG_LEVEL = logging.DEBUG
