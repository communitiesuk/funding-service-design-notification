import logging

from config.envs.default import DefaultConfig as Config
from fsd_utils import configclass


@configclass
class DevConfig(Config):
    """Flask Dev Pipeline Environment Configuration."""

    SECRET_KEY = "dev"  # pragma: allowlist secret
    SESSION_COOKIE_NAME = "session_cookie"

    # Logging
    FSD_LOG_LEVEL = logging.INFO
