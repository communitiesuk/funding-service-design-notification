import pytest
from fsd_utils.config.notify_constants import NotifyConstants

from app.notification.model.notification import Notification


@pytest.mark.skip(reason="Integration test")
@pytest.mark.parametrize(
    "template_type,data_to_send",
    [
        (
            NotifyConstants.TEMPLATE_TYPE_APPLICATION,
            {
                "to": "submitted@unittest.com",
                "full_name": "unit test",
                "content": {
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
            },
        ),
        (
            NotifyConstants.TEMPLATE_TYPE_INCOMPLETE_APPLICATION,
            {
                "to": "incomplete@unittest.com",
                "full_name": "unit test",
                "content": {
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
            },
        ),
    ],
)
def test_send_real_notification(flask_test_client, template_type, data_to_send):
    """
    This is an integration test that hits the real notify service.
    To make this work, unskip it and add the notify API key to pytest.ini
    """
    with flask_test_client.app.app.test_request_context():
        data_to_send["type"] = template_type
        Notification.email_recipient(json_data=data_to_send)
