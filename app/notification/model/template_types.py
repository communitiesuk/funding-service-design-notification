from app.notification.model.notifier import Notifier
from app.notification.model.response import template_type_error
from flask import current_app
from fsd_utils.config.notify_constants import NotifyConstants


def email_recipient(json_data: dict):
    """
    Function matches with the correct template type &
    calls the relevant function from process_data.py.
    """
    match json_data.get("type"):
        case NotifyConstants.TEMPLATE_TYPE_MAGIC_LINK:
            current_app.logger.info(
                f"Validating template type: {json_data.get('type')}")
            return Notifier.send_magic_link(json_data)

        case "APPLICATION_RECORD_OF_SUBMISSION":
            current_app.logger.info(
                f"Validating template type: {json_data.get('type')}")
            return Notifier.send_application(json_data)

        case "NOTIFICATION" | "REMINDER" | "AWARD":
            return f"Currently {json_data.get('type')} service is not available." # noqa

        case _:
            current_app.logger.exception(
                f"Incorrect template type {json_data.get('type')}")
            return template_type_error(json_data)
