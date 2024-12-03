import json
from unittest.mock import ANY

import pytest

from app.notification.application_reminder.map_contents import ApplicationReminder
from app.notification.model.notification import Notification
from app.notification.model.notifier import Notifier
from config import Config
from examplar_data.application_data import expected_application_reminder_json
from examplar_data.application_data import notification_class_data_for_application
from examplar_data.application_data import notification_class_data_for_cof_application
from examplar_data.application_data import notification_class_data_for_eoi
from examplar_data.application_data import unexpected_application_json


@pytest.mark.usefixtures("live_server")
def test_application_contents_with_unexpected_data(flask_test_client):
    """
    GIVEN: our service running on flask test client.
    WHEN: we post application data with no application id
    to the endpoint "/send".
    THEN: we check if it returns an error message.
    """

    response = flask_test_client.post(
        "/send",
        json=unexpected_application_json,
        follow_redirects=True,
    )

    assert response.status_code == 400, "Unexpected status code"


@pytest.mark.usefixtures("live_server")
def test_application_contents_with_none_contents(flask_test_client):
    """
    GIVEN: our service running on flask test client.
    WHEN: we post no data to the endpoint "/send".
    THEN: we check if it returns status code 400.
    """

    response = flask_test_client.post(
        "/send",
        json=None,
        follow_redirects=True,
    )

    assert response.status_code == 400


def test_application_reminder_contents(app_context):
    """
    GIVEN: our service running with app_context fixture.
    WHEN: two separate methods on different classes chained together with given
     expected incoming JSON.
    THEN: we check if expected output is returned.
    """

    expected_json = expected_application_reminder_json
    data = Notification.from_json(expected_json)
    application_class_object = ApplicationReminder.from_notification(data)
    deadline_date = application_class_object.deadline_date

    assert "20 May 2022 at 02:47pm" == deadline_date


def test_format_submission_date(mock_application_class_data):
    application = mock_application_class_data
    response = application.format_submission_date
    assert response == "14 May 2022 at 10:25am"


def testHealthcheckEndpoint(flask_test_client):
    response = flask_test_client.get("/healthcheck")
    expected_dict = {"check_flask_running": "OK"}
    assert expected_dict in response.json()["checks"], "Unexpected json body"


@pytest.mark.parametrize(
    "mock_notify_response",
    ["empty_content", "mock_request_data"],
    indirect=True,
)
def test_send_email(app_context, flask_test_client, mock_notify_response, mock_request_data):
    response = flask_test_client.post("/send", json=mock_request_data)
    assert response.status_code == mock_notify_response[1]  # Check status code from the fixture

    response_data = json.loads(response.content)

    if mock_notify_response[1] == 200:
        assert response_data == {"success": True}
    else:
        assert response_data == {"error": "Invalid request"}


@pytest.mark.parametrize(
    "mock_notifications_api_client",
    [2],
    indirect=True,
)
def test_send_submitted_application(
    app_context,
    mock_notifier_api_client,
    mock_notifications_api_client,
):
    _, code = Notifier.send_submitted_application(
        notification_class_data_for_application(date_submitted=True, deadline_date=False)
    )

    assert code == 200


@pytest.mark.parametrize(
    "mock_notifications_api_client, language, template_id",
    [
        (2, "en", Config.APPLICATION_SUBMISSION_TEMPLATE_ID_EN),
        (2, "cy", Config.APPLICATION_SUBMISSION_TEMPLATE_ID_CY),
    ],
    indirect=["mock_notifications_api_client"],
)
def test_send_submitted_lang(
    app_context,
    mock_notifier_api_client,
    mock_notifications_api_client,
    language,
    template_id,
):
    _, code = Notifier.send_submitted_application(
        notification=notification_class_data_for_cof_application(
            date_submitted=True,
            deadline_date=False,
            language=language,
        )
    )

    mock_notifications_api_client.send_email_notification.assert_called_with(
        email_address=ANY,
        template_id=template_id,
        email_reply_to_id=ANY,
        personalisation=ANY,
        reference=None,
    )

    assert code == 200


@pytest.mark.parametrize(
    "mock_notifications_api_client, language, template_id",
    [
        (3, "en", "705684c7-6985-4d4c-9170-08a85f47b8e1"),
        (3, "cy", "ead6bfc2-f3a1-468c-8d5a-87a32bf31311"),
    ],
    indirect=["mock_notifications_api_client"],
)
def test_send_submitted_eoi(
    app_context,
    mock_notifier_api_client,
    mock_notifications_api_client,
    language,
    template_id,
):
    _, code = Notifier.send_submitted_eoi(
        notification=notification_class_data_for_eoi(
            date_submitted=True,
            deadline_date=False,
            language=language,
            govuk_notify_reference="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        ),
        template_name="Pass with caveats",
    )

    mock_notifications_api_client.send_email_notification.assert_called_with(
        email_address=ANY,
        template_id=template_id,
        email_reply_to_id=ANY,
        personalisation=ANY,
        reference="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
    )

    assert code == 200


@pytest.mark.parametrize(
    "mock_notifications_api_client",
    [2],
    indirect=True,
)
def test_send_incomplete_application(
    app_context,
    mock_notifier_api_client,
    mock_notifications_api_client,
):
    _, code = Notifier.send_submitted_application(
        notification_class_data_for_application(date_submitted=False, deadline_date=False)
    )

    assert code == 200
