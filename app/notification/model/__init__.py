from app.notification.model.template_types import email_recipient
from config import Config
from flask import current_app
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
    print("\n")
    current_app.logger.debug("Entry point - incoming data")

    notify_response = email_recipient(notification_data)
    current_app.logger.debug("Email Successfully Sent")
    print("\n")
    return notify_response
