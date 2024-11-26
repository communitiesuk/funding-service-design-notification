import pytest
from fsd_utils.config.notify_constants import NotifyConstants

from app.notification.model.notification import Notification
from app.notification.model.notifier import Notifier


@pytest.mark.skip(reason="Integration test")
def test_send_notification(flask_test_client):
    """
    This is an integration test that hits the real notify service.
    To make this work, unskip it and add the notify API key to pytest.ini
    """
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
                "prospectus_url": "https://google.com",
            },
            NotifyConstants.MAGIC_LINK_CONTACT_HELP_EMAIL_FIELD: "FundingService@communities.gov.uk",
        },
    )
    with flask_test_client.app.app.test_request_context():
        _, code = Notifier.send_submitted_application(notification=notification)
        assert code == 200
