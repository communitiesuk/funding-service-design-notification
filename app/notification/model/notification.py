from dataclasses import dataclass


@dataclass
class Notification:
    """
    Class processes notification data.
    Returns:
        notification class object.
    """

    template_type: str
    contact_info: str
    content: str

    @staticmethod
    def from_json(data):
        """
        Function initialise the data by checking the required format
        of the data which must contain keys("type", "content", "to")
        & required values then
        Function will be  called in relevant services to map
        the incoming data from external services otherwise return the
        error by relevant service based on given "template_type".
        """
        if "" not in data.values() and None not in data.values():
            notification_data = Notification(
                template_type=data["type"],
                contact_info=data["to"],
                content=data["content"],
            )
            return notification_data
