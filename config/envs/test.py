from fsd_utils import configclass

from config.envs.default import DefaultConfig as Config


@configclass
class TestConfig(Config):
    """Flask Test Environment Configuration."""

    pass
