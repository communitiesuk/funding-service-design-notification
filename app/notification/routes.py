import json

from app.config import API_KEY
from app.notification.models.data import email_recipient
from app.notification.models.data import get_example_data
from app.notification.models.notification import Notification
from flask import Blueprint
from flask import request
from notifications_python_client.notifications import NotificationsAPIClient

notifications_client = NotificationsAPIClient(API_KEY)

notification_bp = Blueprint(
    "notification_bp",
    __name__,
    url_prefix="/send",
    template_folder="templates",
)


@notification_bp.route("/", methods=["POST", "GET"])
def send_notification() -> dict:
    """
    route accepts POST request with json data.
    Json data integrates with gov-uk notify service
    to send contents from json data to recipient.

    Returns:
        dict: if data received, recipient's contact info & access link.
    """
    example_data = json.dumps(get_example_data(), indent=2)
    notification_data = request.get_json()

    if notification_data:
        send_email = email_recipient(
            data=notification_data,
            example_data=example_data,
            notification_class=Notification,
        )
        return send_email

    else:

        return (
            "Bad request. No data has been received. Please check the"
            " contents of the notification data:"
            f" {notification_data}\n\nExample data: {example_data})"
        )
