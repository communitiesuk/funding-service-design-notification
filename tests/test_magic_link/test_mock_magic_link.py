from unittest import mock

import pytest
from app.notification.model import send_email
from tests.test_magic_link.magic_link_data import expected_magic_link_response


@pytest.mark.usefixtures("live_server")
@pytest.mark.usefixtures("mocked_magic_link")
@mock.patch("app.notification.model.send_email")
def test_mocked_magic_link(mock_send_email):
    """
    GIVEN: our service running on unittest mock & pytest-mock library.
    WHEN: (a) we mock expected magic_link json & response contents.
        : (b) we make a call to "send_email()" function.
    THEN: (a) we check  "send_email()" returns the
        expected mocked contents.
    """

    mock_send_email.return_value = expected_magic_link_response
    email_response = send_email()
    assert "MAGIC-LINK-GOES-HERE" in email_response[0][0]["content"]["body"]
