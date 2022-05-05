import json

from app.config import API_KEY
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
        if notification_data.get("type") == "MAGIC_LINK":
            magic_link = Notification.send_magic_link(notification_data)
            return magic_link
        elif notification_data.get("type") == "NOTIFICATION":
            return (
                f"Currently {notification_data['type']} service is not"
                " available."
            )
        elif notification_data.get("type") == "REMINDER":
            return (
                f"Currently {notification_data['type']} service is not"
                " available."
            )
        elif notification_data.get("type") == "AWARD":
            return (
                f"Currently {notification_data['type']} service is not"
                " available."
            )
        else:
            return (
                "Bad request, please check the contents of the notification"
                f" data: {notification_data}.\n\nExpected type:('MAGIC_LINK'"
                " or 'NOTIFICATION' or 'REMINDER' or 'AWARD' )\n\nExample"
                f" data: {example_data}"
            )
    else:
        return (
            "Bad request, please check the contents of the notification data:"
            f" {notification_data}\n\nExample data: {example_data})"
        )
