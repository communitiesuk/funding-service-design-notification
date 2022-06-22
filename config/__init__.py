import os

FLASK_ENV = os.environ.get("FLASK_ENV")

if not FLASK_ENV:
    raise KeyError("FLASK_ENV does not exist in environ")

match FLASK_ENV:
    case "development":
        from config.development import DevelopmentConfig as Config  # noqa
    case "unit_test":
        from config.unit_test import UnitTestConfig as Config  # noqa
    case _:
        from config.default import DefaultConfig as Config  # noqa

try:
    Config.pretty_print()
except AttributeError:
    print({"msg": "Config doesn't have pretty_print function."})

__all__ = [Config]
