from unittest import mock

import pytest
from app.notification.model.notifier import Notifier
from app.notification.model.routes import send_email
from tests.test_magic_link.magic_link_data import email_recipient_data
from tests.test_magic_link.magic_link_data import expected_magic_link_data
from tests.test_magic_link.magic_link_data import make_response_data


# PLEASE REVIEW THIS TEST, IF IT IS OK THEN I CAN RE-WRITE ALL THE TESTS WITH MOCK DATA/RESPONSE. # noqa
# TEST DOES NOT REQUIRE NETWORK.


@pytest.mark.usefixtures("live_server")
@mock.patch("app.notification.model.routes.request.get_json")
@mock.patch("app.notification.model.routes.email_recipient")
@mock.patch(
    "app.notification.model.notifier.notifications_client.send_email_notification"  # noqa
)
@mock.patch("app.notification.model.routes.make_response")
def test_mock_magic_link(
    mock_make_response,
    mock_notifications_client,
    mock_email_recipient,
    mock_request_get_json,
):

    # Mock return value of "request.get_json()" to "expected_magic_link_data"  # noqa
    mock_request_get_json.return_value = expected_magic_link_data
    # Mock return value of notification_client to "email_recipient_data" # noqa
    mock_notifications_client.return_value = email_recipient_data
    # Mock return value of app.notification.model.routes.make_response to make_response_data  # noqa
    mock_make_response.return_value = make_response_data

    # Call send_email() route & check response == mock_make_response.return_value # noqa
    response_send_email = send_email()
    assert response_send_email == mock_make_response.return_value
    # Check if the email_recipient from route send_email() func was called once & with expected_magic_link_data # noqa
    mock_email_recipient.assert_called_once()
    mock_email_recipient.assert_called_once_with(expected_magic_link_data)
    # Check if the sent content exists in the send_email response
    assert (
        "MAGIC-LINK-GOES-HERE"
        in response_send_email["notify_response"]["content"]["body"]
    )

    # Call Notifier.send_magic_link with expected_magic_link_data & check response == email_recipient_data  # noqa
    response_send_magic_link = Notifier.send_magic_link(
        expected_magic_link_data
    )
    assert response_send_magic_link == email_recipient_data
    # Check if the Notifier.send_magic_link function was called once & with expected magic link data  # noqa
    mock_notifications_client.assert_called_once()
    mock_notifications_client.assert_called_once_with(
        template_id="02a6d48a-f227-4b9a-9dd7-9e0cf203c8a2",
        email_address="test_recipient@email.com",
        personalisation={
            "name of fund": "FUND NAME GOES HERE",
            "link to application": "MAGIC-LINK-GOES-HERE",
            "contact details": "dummy_contact_info@funding-service-help.com",
        },
    )
