from fsd_utils.config.notify_constants import NotifyConstants

from app.notification.model.notification import Notification
from app.notification.model.notifier import Notifier


def test_send_notification(flask_test_client):
    notification = Notification(
        template_type="APPLICATION_RECORD_OF_SUBMISSION",
        contact_info="recipient@unittest.com",
        contact_name="unit test",
        content={
            NotifyConstants.APPLICATION_FIELD: {
                "fund_name": "unit test fund",
                "round_name": "unit test round",
                "questions_file": "dGhpcyBpcyBhIHRlc3Q=",
                "date_submitted": "2024-11-26T11:23:03.000",
                "fund_id": "asdf-wer-234-asdf",
                "reference": "TEST-ABC",
                "language": "en",
            },
            NotifyConstants.MAGIC_LINK_CONTACT_HELP_EMAIL_FIELD: "FundingService@communities.gov.uk",
        },
    )
    with flask_test_client.app.app.test_request_context():
        response, code = Notifier.send_submitted_application(notification=notification)
        assert code == 200
