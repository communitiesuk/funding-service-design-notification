import os

FLASK_ENV = os.environ.get("FLASK_ENV")

if not FLASK_ENV:
    raise KeyError("FLASK_ENV does not exist in environ")

match FLASK_ENV:
    case "development":
        from config.environments.development import (  # noqa
            DevelopmentConfig as Config,  # noqa
        )  # noqa
    case "unit_test":
        from config.environments.unit_test import (  # noqa
            UnitTestConfig as Config,  # noqa
        )  # noqa
    case _:
        from config.environments.default import DefaultConfig as Config  # noqa

try:
    Config.pretty_print()
except AttributeError:
    print({"msg": "Config doesn't have pretty_print function."})

__all__ = [Config]
