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
        400: if data is  not received or in incorrect format, returns 400.
    """
    notification_data = request.get_json()
    data = Notification.process_notification_data(notification_data)

    if data:
        if data.template_type == "MAGIC_LINK":
            magic_link = Notification.send_magic_link(
                contact_info=data.contact_info,
                content=data.content,
            )
            return magic_link

        elif data.template_type == "NOTIFICATION":
            return f"Currently {data.template_type} service is not available."
        elif data.template_type == "REMINDER":
            return f"Currently {data.template_type} service is not available."

        elif data.template_type == "AWARD":
            return f"Currently {data.template_type} service is not available."

        else:
            return (
                "Please check value of the 'type' key.\nExpected"
                " types:('MAGIC_LINK' or 'NOTIFICATION' or 'REMINDER' or"
                " 'AWARD' )"
            )
    else:
        example_data = json.dumps(get_example_data(), indent=2)
        return (
            "Bad request, please check the contents of the notification data:"
            f" {notification_data}\nExample data: {example_data})"
        )
