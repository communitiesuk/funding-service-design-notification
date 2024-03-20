from os import environ

from config.envs.default import DefaultConfig as Config
from fsd_utils import configclass


@configclass
class TestConfig(Config):
    """Flask Test Environment Configuration."""

    SECRET_KEY = environ.get("SECRET_KEY", "test")
