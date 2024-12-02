import logging

from fsd_utils import configclass

from config.envs.default import DefaultConfig


@configclass
class UnitTestConfig(DefaultConfig):
    #  Application Config
    SECRET_KEY = "dev"  # pragma: allowlist secret
    SESSION_COOKIE_NAME = "session_cookie"

    # Logging
    FSD_LOG_LEVEL = logging.DEBUG

    REPLY_TO_EMAILS_WITH_NOTIFY_ID = {
        "FundingService@communities.gov.uk": "10668b8d-9472-4ce8-ae07-4fcc7bf93a9d",
        "nope@wrong.gov.uk": "100",
        "COF@communities.gov.uk": "10668b8d-9472-4ce8-ae07-4fcc7bf93a9d",
        "transformationfund@levellingup.gov.uk": ("25286d9a-8543-41b5-a00f-331b999e51f0"),
    }

    # ---------------
    # Task Executor Config
    # ---------------
    TASK_EXECUTOR_MAX_THREAD = 5  # max amount of threads
    # ---------------
    # AWS Overall Config
    # ---------------
    AWS_ACCESS_KEY_ID = "test_access_id"
    AWS_SECRET_ACCESS_KEY = "test_secret_key"  # pragma: allowlist secret
    AWS_REGION = "eu-west-2"

    # ---------------
    # S3 Config
    # ---------------
    AWS_MSG_BUCKET_NAME = "fsd-notification-bucket"

    # ---------------
    # SQS Config
    # ---------------
    SQS_WAIT_TIME = 2  # max time to wait (in sec) before returning
    SQS_BATCH_SIZE = 10  # MaxNumber Of Messages to process
    SQS_VISIBILITY_TIME = 1  # time for message to temporarily invisible to others (in sec)
    SQS_RECEIVE_MESSAGE_CYCLE_TIME = 5  # Run the job every 'x' seconds
    AWS_SQS_NOTIF_APP_PRIMARY_QUEUE_URL = None
