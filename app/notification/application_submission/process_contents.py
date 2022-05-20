import json
import os
from dataclasses import dataclass
from datetime import datetime

from app.config import FLASK_ROOT
from app.notification.models.notification import NotificationData


def get_data():
    """This is a dummy data for data mapping.
    TO BE DELETED ONCE INTEGRATED WITH AUTHENTICATOR SERVICE.
    """
    file_path = os.path.join(
        FLASK_ROOT,
        "app",
        "notification",
        "application_submission",
        "dummy_data.json",
    )

    json_data = open(file_path)
    json.load(json_data)
    json_data.close()


get_data()


@dataclass
class ProcessApplicationData:
    questions: dict
    answers: dict
    submission_date: datetime
    fund_name: dict
    fund_round: dict
    application_id: dict

    @staticmethod
    def get_questions(json_data):
        notification_data = NotificationData.notification_data(json_data)
        print(notification_data)
        pass

    def get_answers(json_data):
        pass
