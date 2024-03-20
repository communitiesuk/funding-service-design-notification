from os import environ

from fsd_utils import configclass

from config.envs.default import DefaultConfig as Config


@configclass
class TestConfig(Config):
    """Flask Test Environment Configuration."""

    SECRET_KEY = environ.get("SECRET_KEY", "test")
