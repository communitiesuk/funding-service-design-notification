# from app.notification.model.template_types import email_recipient
from app.notification.model.notification import Notification
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
        dict: requested contents to the assessor /applicant.
    """
    notification_data = request.get_json()

    notify_response = Notification.email_recipient(notification_data)
    return notify_response
