from dataclasses import dataclass


@dataclass
class _NotificationContents:
    contact_info: str
    contact_name: str
    fund_name: str
