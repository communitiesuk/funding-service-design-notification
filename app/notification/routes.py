from app.config import API_KEY
from app.config import TEMPLATE_ID
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
    route accepts post request, loads json data
    & json data integrates with gov-uk notify service
    to send magic link from json data to the recipient

    Returns:
        dict: recipient contact info, type of link & magic link
    """
    notification_data = request.get_json()
    data = Notification.process_notification_data(notification_data)

    response = notifications_client.send_email_notification(
        email_address=data.contact_info,
        template_id=TEMPLATE_ID,
        personalisation={
            "SUBJECT": "Funding service link",
            "MAGIC_LINK": data.content,
        },
    )

    return response
