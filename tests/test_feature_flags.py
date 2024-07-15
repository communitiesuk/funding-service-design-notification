import unittest

from app.feature_flag.feature_flags import FeatureFlags
from app.feature_flag.feature_flags import HandleFeatureFlags
from config import Config


class TestFeatureFlags(unittest.TestCase):

    def test_get_feature_flag_sqs_extended_client_for_environments(self):
        Config.FLASK_ENV = "dev"
        assert HandleFeatureFlags.get_flag(FeatureFlags.SQS_EXTENDED_CLIENT_FEATURE) is True

        Config.FLASK_ENV = "development"
        assert HandleFeatureFlags.get_flag(FeatureFlags.SQS_EXTENDED_CLIENT_FEATURE) is True

        Config.FLASK_ENV = "test"
        assert HandleFeatureFlags.get_flag(FeatureFlags.SQS_EXTENDED_CLIENT_FEATURE) is True

        Config.FLASK_ENV = "uat"
        assert HandleFeatureFlags.get_flag(FeatureFlags.SQS_EXTENDED_CLIENT_FEATURE) is False

        Config.FLASK_ENV = "production"
        assert HandleFeatureFlags.get_flag(FeatureFlags.SQS_EXTENDED_CLIENT_FEATURE) is False
