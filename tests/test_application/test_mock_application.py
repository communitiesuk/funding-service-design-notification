from unittest import mock

import pytest
from app.notification.model import send_email
from examplar_data.application_data import (
    expected_application_response,
)


@pytest.mark.usefixtures("live_server")
@pytest.mark.usefixtures("mocked_application")
@mock.patch("app.notification.model.send_email")
def test_mocked_application(mock_send_email):
    """
    GIVEN: our service running on unittest mock & pytest-mock library.
    WHEN: (a) we mock expected application json & response contents.
        : (b) we make a call to "send_email()" function.
    THEN: (a) we check  "send_email()" returns the
        expected mocked contents.
    """

    mock_send_email.return_value = expected_application_response
    email_response = send_email()
    assert (
        "Fund name:  Funding service"
        in email_response[0][0]["content"]["body"]
    )
