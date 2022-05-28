from app.config import API_KEY
from app.notification.model.exceptions import NotificationError
from app.notification.model.template_types import email_recipient
from flask import Blueprint
from flask import make_response
from flask import request
from notifications_python_client.notifications import NotificationsAPIClient
from requests import Response

notifications_client = NotificationsAPIClient(API_KEY)

notification_bp = Blueprint(
    "notification_bp",
    __name__,
    url_prefix="/send",
    template_folder="templates",
)


@notification_bp.route("", methods=["POST"])
def send_email() -> Response:
    """
    route accepts POST request with json data.
    Json data integrates with gov-uk notify service
    to send contents from json data to recipient.

    Returns:
        dict: if data received, recipient's contact info & access link.
    """
    notification_data = request.get_json()
    if notification_data:
        try:
            notify_response = email_recipient(notification_data)
            return make_response(
                {"notify_response": notify_response, "status": "ok"}, 200
            )
        except NotificationError as e:

            return make_response(
                {"message": e.message, "status": "Error"}, 400
            )

    else:
        return make_response(
            {
                "message": (
                    "Bad request. No data has been received.Please check the"
                    " contents of the notification data:"
                    f"{notification_data}"
                ),
                "status": "Error",
            },
            400,
        )
