from app.config import API_KEY
from app.config import EMAIL_ADDRESS
from app.config import TEMPLATE_ID
from flask import Blueprint
from notifications_python_client.notifications import NotificationsAPIClient

notification_bp = Blueprint(
    "notification_bp",
    __name__,
    url_prefix="/send",
    template_folder="templates",
)

notifications_client = NotificationsAPIClient(API_KEY)


@notification_bp.route("/")
def send_notification():
    email_address = EMAIL_ADDRESS
    template_id = TEMPLATE_ID
    response = notifications_client.send_email_notification(
        email_address=email_address,
        template_id=template_id,
    )
    return response
