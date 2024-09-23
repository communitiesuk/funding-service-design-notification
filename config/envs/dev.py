import logging

from fsd_utils import configclass

from config.envs.default import DefaultConfig as Config


@configclass
class DevConfig(Config):
    """Flask Dev Pipeline Environment Configuration."""

    SESSION_COOKIE_NAME = "session_cookie"

    # Logging
    FSD_LOG_LEVEL = logging.INFO
