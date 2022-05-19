from app.notification.custom_exceptions import NotificationError


def email_recipient(data: dict, example_data: dict, notification_class):
    if data.get("type") == "MAGIC_LINK":
        magic_link = notification_class.send_magic_link(data)
        return magic_link
    elif data.get("type") == "NOTIFICATION":
        return f"Currently {data.get('type')} service is not available."
    elif data.get("type") == "REMINDER":
        return f"Currently {data.get('type')} service is not available."
    elif data.get("type") == "AWARD":
        return f"Currently {data.get('type')} service is not available."
    else:
        raise NotificationError(
            message=(
                "Incorrect type, please check the key 'type' & other keys,"
                f" values from notification data: {data}.\n\nExpected"
                " type:('MAGIC_LINK' or 'NOTIFICATION' or 'REMINDER' or"
                f" 'AWARD' )\n\nExample data: {example_data}"
            )
        )
