from app.notification.model.notifier import Notifier
from app.notification.model.response import template_type_error


def email_recipient(json_data: dict):
    """
    Function matches with the correct template type &
    calls the relevant function from process_data.py.
    """
    match json_data.get("type"):
        case "MAGIC_LINK":
            return Notifier.send_magic_link(json_data)

        case "APPLICATION_RECORD_OF_SUBMISSION":
            return Notifier.send_application(json_data)

        case "NOTIFICATION" | "REMINDER" | "AWARD":
            return f"Currently {json_data.get('type')} service is not available." # noqa

        case _:
            return template_type_error(json_data)
