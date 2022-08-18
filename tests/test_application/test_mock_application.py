from unittest import mock

import pytest
from app.notification.model.notifier import Notifier
from app.notification.model.routes import send_email
from examplar_data.application_data import expected_application_data
from examplar_data.application_data import (
    expected_application_response,
)


@pytest.mark.usefixtures("live_server")
@pytest.mark.usefixtures("mocked_application")
@mock.patch("app.notification.model.routes.email_recipient")
def test_mocked_application(mock_email_recipient_func):
    """
    GIVEN: our service running on unittest mock & pytest-mock library.
    WHEN: (a) we post expected application mock data to the endpoint "/send".
        : (b) we make a call to govuk-notify-service with
        expected application data.
    THEN: (a) we check route "send_email()" returns the
        expected mocked contents & status "ok" represent 200.
        : (b) we check "Notifier.send_application" returns the
         expected mock contents.
    """

    send_email_route_response = send_email()
    assert (
        "Jack-Simon"
        in send_email_route_response["notify_response"]["content"]["body"]
    )
    assert "ok" in send_email_route_response["status"]
    mock_email_recipient_func.assert_called_once()

    response_from_notify_service = Notifier.send_application(
        expected_application_data
    )
    assert (
        response_from_notify_service
        == expected_application_response["notify_response"]
    )
