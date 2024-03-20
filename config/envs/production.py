from config.envs.default import DefaultConfig as Config
from fsd_utils import configclass


@configclass
class ProductionConfig(Config):
    """Flask Production Environment Configuration."""

    pass
