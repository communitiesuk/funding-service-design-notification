# flake8: noqa
import os

FLASK_ENV = os.environ.get("FLASK_ENV")

if not FLASK_ENV:
    raise KeyError("FLASK_ENV does not exist in environ")

match FLASK_ENV:
    case "development":
        from config.envs.development import DevelopmentConfig as Config
    case "unit_test":
        from config.envs.unit_test import UnitTestConfig as Config
    case "dev":
        from config.envs.dev import DevConfig as Config
    case "test":
        from config.envs.test import TestConfig as Config
    case "production":
        from config.envs.production import ProductionConfig as Config
    case _:
        from config.envs.default import DefaultConfig as Config


try:
    Config.pretty_print()
except AttributeError:
    print({"msg": "Config doesn't have pretty_print function."})

__all__ = [Config]
