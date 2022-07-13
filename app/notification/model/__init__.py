from app.notification.model.template_types import email_recipient
from config import Config
from flask import request
from notifications_python_client.notifications import NotificationsAPIClient
from requests import Response

notifications_client = NotificationsAPIClient(Config.GOV_NOTIFY_API_KEY)


def send_email() -> Response:
    """
    Function accepts POST request with json contents.
    Given json integrates with gov-uk notify service
    to send requested contents to the recipient.

    Returns:
        dict: if data received, recipient's contact info & access link.
    """
    notification_data = request.get_json()

    notify_response = email_recipient(notification_data)
    return notify_response
