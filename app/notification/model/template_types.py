from app.notification.model.exceptions import NotificationError
from app.notification.model.notifier import Notifier


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
            raise NotificationError(
                message=(
                    "Incorrect type, please check the key 'type' & other keys,"
                    f" values from notification data: {json_data}.\n\nExpected"
                    " type:('MAGIC_LINK' or 'NOTIFICATION' or 'REMINDER' or"
                    f" 'AWARD' or 'APPLICATION_RECORD_OF_SUBMISSION')." # noqa
                )
            )
