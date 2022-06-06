from unittest import mock

import pytest
from app.notification.model.notifier import Notifier
from app.notification.model.routes import send_email
from tests.test_magic_link.magic_link_data import email_recipient_data
from tests.test_magic_link.magic_link_data import expected_magic_link_data
from tests.test_magic_link.magic_link_data import (
    incorrect_template_type_value_data,
)
from tests.test_magic_link.magic_link_data import make_response_data


@pytest.mark.usefixtures("live_server")
@pytest.mark.usefixtures("mocked_magic_link_successful")
@mock.patch("app.notification.model.routes.email_recipient")
def test_mocked_magic_link(mock_email_recipient):

    response_send_email = send_email()
    assert response_send_email == make_response_data
    assert (
        "MAGIC-LINK-GOES-HERE"
        in response_send_email["notify_response"]["content"]["body"]
    )
    mock_email_recipient.assert_called_once()
    response_notify_service = Notifier.send_magic_link(
        expected_magic_link_data
    )
    assert response_notify_service == email_recipient_data


@pytest.mark.usefixtures("live_server")
@mock.patch("app.notification.model.routes.request.get_json")
@mock.patch("app.notification.model.routes.email_recipient")
def test_mocked_magic_link_incorrect_type(
    mock_email_recipient, mock_request_get_json
):

    mock_request_get_json.return_value = incorrect_template_type_value_data

    mock_email_recipient.return_value = (
        "Incorrect type, please check the key 'type' & other keys, values"
        " from notification data:"
        f" {incorrect_template_type_value_data}.\n\nExpected"
        " type:('MAGIC_LINK' or 'NOTIFICATION' or 'REMINDER' or 'AWARD' or"
        " 'APPLICATION_RECORD_OF_SUBMISSION')."
    )

    email_response = send_email()
    mock_email_recipient.assert_called_once()
    assert (
        email_response.json["notify_response"]
        == mock_email_recipient.return_value
    )
