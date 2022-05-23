from app.notification.custom_exceptions import NotificationError


def email_recipient(data: dict, example_data: dict, notification_class):
    """
    Function matches with the correct template type &
    calls the relevant function from process_notification_data.py.
    """
    match data.get("type"):
        case "MAGIC_LINK":
            return notification_class.send_magic_link(data)

        case "APPLICATION_RECORD_OF_SUBMISSION":
            return notification_class.send_application(data)

        case "NOTIFICATION" | "REMINDER" | "AWARD":
            return f"Currently {data.get('type')} service is not available."

        case _:
            raise NotificationError(
                message=(
                    "Incorrect type, please check the key 'type' & other keys,"
                    f" values from notification data: {data}.\n\nExpected"
                    " type:('MAGIC_LINK' or 'NOTIFICATION' or 'REMINDER' or"
                    f" 'AWARD' or 'APPLICATION_RECORD_OF_SUBMISSION')\n\nExample data: {example_data}" # noqa
                )
            )