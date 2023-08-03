import json

import pytest
from app.notification.application.map_contents import Application
from app.notification.application_reminder.map_contents import (
    ApplicationReminder,
)
from app.notification.model.notification import Notification
from examplar_data.application_data import expected_application_data
from examplar_data.application_data import (
    expected_application_reminder_data,
)
from examplar_data.application_data import (
    unexpected_application_data,
)


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
        json=unexpected_application_data,
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


def test_application_map_contents_response(app_context):
    """
    GIVEN: our service running with app_context fixture.
    WHEN: two separate methods on different classes chained together with given
     expected incoming JSON.
    THEN: we check if expected output is returned.
    """

    expected_json = expected_application_data
    data = Notification.from_json(expected_json)
    application_class_object = Application.from_notification(data)
    questions = application_class_object.questions

    assert "Jack-Simon" in questions.getvalue().decode()
    assert "Yes" in questions.getvalue().decode()
    assert "No" in questions.getvalue().decode()


def test_application_reminder_contents(app_context):
    """
    GIVEN: our service running with app_context fixture.
    WHEN: two separate methods on different classes chained together with given
     expected incoming JSON.
    THEN: we check if expected output is returned.
    """

    expected_json = expected_application_reminder_data
    data = Notification.from_json(expected_json)
    application_class_object = ApplicationReminder.from_notification(data)
    fund_deadline = application_class_object.deadline_date

    assert "20 May 2022 at 02:47pm" == fund_deadline


def test_format_submission_date(application_class_data):
    application = application_class_data
    response = application.format_submission_date
    assert response == "14 May 2022 at 10:25am"


def testHealthcheckEndpoint(flask_test_client):
    response = flask_test_client.get("/healthcheck")
    expected_dict = {"check_flask_running": "OK"}
    assert expected_dict in response.json["checks"], "Unexpected json body"


@pytest.mark.parametrize(
    "mock_notify_response",
    ["empty_content", "mock_request_data"],
    indirect=True,
)
def test_send_email(app_context, flask_test_client, mock_notify_response):
    response = flask_test_client.post("/send")
    assert (
        response.status_code == mock_notify_response[1]
    )  # Check status code from the fixture

    response_data = response.get_data(as_text=True)
    response_data = json.loads(response_data)

    if mock_notify_response[1] == 200:
        assert response_data == {"success": True}
    else:
        assert response_data == {"error": "Invalid request"}
