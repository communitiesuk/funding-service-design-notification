from os import getenv

from app.notification.model.notification import Notification
from config import Config
from fsd_utils.services.aws import SQSClient


_SQS_CLIENT = SQSClient(
    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
    region_name=Config.AWS_REGION,
    endpoint_url=getenv("AWS_ENDPOINT_OVERRIDE", None),
)

_NOTIFICATION_QUEUE = getenv("AWS_SQS_NOTIFICATION_QUEUE_NAME", "fsd-queue-notification")
_SQS_QUEUE_URL = Config.AWS_PRIMARY_QUEUE_URL or _SQS_CLIENT.get_queue_url(_NOTIFICATION_QUEUE)


def read_and_process_from_notify_queue():
    from app import app

    queued_notifications = _SQS_CLIENT.receive_messages(
        _SQS_QUEUE_URL,
        Config.SQS_BATCH_SIZE,
        Config.SQS_VISIBILITY_TIME,
        Config.SQS_WAIT_TIME
    )

    if not queued_notifications:
        return

    with app.app_context():
        for raw_notification in queued_notifications:
            parsed_notification = Notification.from_json(raw_notification)
            parsed_notification.email_recipient()
