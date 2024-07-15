from enum import Enum

from config import Config


class FeatureFlags(Enum):
    SQS_EXTENDED_CLIENT_FEATURE = {"dev": True, "development": True, "test": True, "uat": False, "production": False}


class HandleFeatureFlags:

    @staticmethod
    def print_flags():
        for flag in FeatureFlags:
            print(f"Feature flag [{flag.name}] --> [{flag.value.get(Config.FLASK_ENV)}] env [{Config.FLASK_ENV}]")

    @staticmethod
    def get_flag(feature_flag: FeatureFlags) -> bool:
        if feature_flag is None:
            return False
        flag_details = feature_flag.value.get(Config.FLASK_ENV)
        if flag_details is None:
            return False
        print(f"Feature flag found and returning the status flag name [{feature_flag.name}] value [{flag_details}]")
        return flag_details
