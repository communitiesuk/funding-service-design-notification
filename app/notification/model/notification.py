from dataclasses import dataclass


@dataclass
class Notification:
    template_type: str
    contact_info: str
    content: dict

    @staticmethod
    def from_json(data: dict):
        """
        Function will be  called in relevant services to map
        the json contents
        """
        notification_data = Notification(
            template_type=data.get("type"),
            contact_info=data.get("to"),
            content=data.get("content"),
        )
        return notification_data
