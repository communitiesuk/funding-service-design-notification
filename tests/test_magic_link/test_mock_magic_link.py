from unittest import mock

import pytest
from app.notification.model.notifier import Notifier
from app.notification.model.routes import send_email
from examplar_data.magic_link_data import expected_magic_link_data
from examplar_data.magic_link_data import expected_magic_link_response
from examplar_data.magic_link_data import incorrect_content_key_data
from examplar_data.magic_link_data import (
    incorrect_template_type_data,
)


@pytest.mark.usefixtures("live_server")
@pytest.mark.usefixtures("mocked_magic_link")
@mock.patch("app.notification.model.routes.email_recipient")
def test_mocked_magic_link(mock_email_recipient_func):
    """
    GIVEN: our service running on unittest mock & pytest-mock library.
    WHEN: (a) we post expected mock data to the endpoint "/send".
        : (b) we make a call to govuk-notify-service with
        expected magic link data.
    THEN: (a) we check route "send_email()" returns the
        expected mocked contents & status "ok" represent 200.
        : (b) we check "Notifier.send_magic_link" returns the
         expected mock contents.
    """

    send_email_route_response = send_email()
    assert (
        "MAGIC-LINK-GOES-HERE"
        in send_email_route_response["notify_response"]["content"]["body"]
    )
    assert "ok" in send_email_route_response["status"]
    mock_email_recipient_func.assert_called_once()

    response_from_notify_service = Notifier.send_magic_link(
        expected_magic_link_data
    )
    assert (
        response_from_notify_service
        == expected_magic_link_response["notify_response"]
    )


@pytest.mark.usefixtures("live_server")
@mock.patch("app.notification.model.routes.request.get_json")
@mock.patch("app.notification.model.routes.email_recipient")
def test_mocked_magic_link_incorrect_type(
    mock_email_recipient_func, mock_request_get_json
):
    """
    GIVEN: our service running on unittest mock library.
    WHEN: we post incorrect template type to endpoint "/send".
    THEN: we check route "send_email()" returns an expected error message.
    """

    mock_request_get_json.return_value = incorrect_template_type_data

    mock_email_recipient_func.return_value = (
        "Incorrect type, please check the key 'type' & other keys, values"
        " from notification data:"
        f" {incorrect_template_type_data}.\n\nExpected"
        " type:('MAGIC_LINK' or 'NOTIFICATION' or 'REMINDER' or 'AWARD' or"
        " 'APPLICATION_RECORD_OF_SUBMISSION')."
    )

    send_email_route_response = send_email()

    mock_email_recipient_func.assert_called_once()

    assert (
        send_email_route_response.json["notify_response"]
        == mock_email_recipient_func.return_value
    )


@pytest.mark.usefixtures("live_server")
@mock.patch("app.notification.model.routes.request.get_json")
@mock.patch("app.notification.model.notifier.Notifier.send_magic_link")
@mock.patch("app.notification.model.routes.email_recipient")
def test_mocked_magic_link_incorrect_key(
    mock_email_recipient_func, mock_send_magic_link_func, mock_request_get_json
):
    """
    GIVEN: our service running on unittest mock library.
    WHEN: (a) we call send_magic_link func & set return value to error message.
        : (b) we post incorrect key from expected data to endpoint "/send".
    THEN: (a) we check if send_magic_link func has been called with
        incorrect_data.
          (b) we check route "send_email()" returns an expected error message.
    """

    mock_request_get_json.return_value = incorrect_content_key_data

    mock_send_magic_link_func.return_value = (
        "Incorrect MAGIC LINK data, please check the contents of"
        " the MAGIC LINK data. \nExample data:"
        f" {expected_magic_link_data}"
    )

    Notifier.send_magic_link(incorrect_content_key_data)
    mock_send_magic_link_func.assert_called_with(incorrect_content_key_data)

    mock_email_recipient_func.return_value = (
        mock_send_magic_link_func.return_value
    )
    send_email_route_response = send_email()
    mock_email_recipient_func.assert_called_once()
    assert (
        send_email_route_response.json["notify_response"]
        == mock_email_recipient_func.return_value
    )
