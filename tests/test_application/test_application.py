import pytest
from app.notification.application.application_utils import remove_html_tags
from app.notification.application.map_contents import Application
from app.notification.application_reminder.map_contents import (
    ApplicationReminder,
)
from app.notification.model.notification import Notification
from examplar_data.application_data import expected_application_data
from examplar_data.application_data import (
    expected_application_data_contains_none_answers,
)
from examplar_data.application_data import (
    expected_application_reminder_data,
)
from examplar_data.application_data import (
    unexpected_application_data,
)


@pytest.mark.usefixtures("live_server")
def test_application_contents_with_expected_data(flask_test_client):
    """
    GIVEN: our service running on flask test client.
    WHEN: we post expected application data to the endpoint "/send".
    THEN: we check if the contents of the message is successfully delivered
    along with the pre-added template message.
    """

    response = flask_test_client.post(
        "/send",
        json=expected_application_data,
        follow_redirects=True,
    )

    assert b"Fund name:  Community Ownership Fund" in response.data
    assert b"Application submitted: 14 May 2022 at 10:25am." in response.data
    assert response.status_code == 200


@pytest.mark.usefixtures("live_server")
def test_application_contents_with_expected_data_containing_none_answers(
    flask_test_client,
):
    """
    GIVEN: our service running on flask test client.
    WHEN: we post expected application data containing null answers to the endpoint "/send". # noqa: E501
    THEN: we check if the contents of the message is successfully delivered
    along with the pre-added template message.
    """

    response = flask_test_client.post(
        "/send",
        json=expected_application_data_contains_none_answers,
        follow_redirects=True,
    )

    assert b"Fund name:  Community Ownership Fund" in response.data
    assert b"Application submitted: 14 May 2022 at 03:25pm." in response.data
    assert response.status_code == 200


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


@pytest.mark.parametrize(
    "input_value, expected_response",
    [
        ("<p> Hello world </p>", "Hello world"),
        ("<ul><li>Item 1</li><li>Item 2</li></ul>", "- Item 1\n     - Item 2"),
        (
            "<ol><li>Item 1</li><li>Item 2</li></ol>",
            "1. Item 1\n     2. Item 2",
        ),
        ("text without html tags", "text without html tags"),
        (None, None),
        (["one", "two"], ["one", "two"]),
        (True, True),
    ],
)
def test_remove_html_tags(app_context, input_value, expected_response):

    response = remove_html_tags(input_value)
    assert response == expected_response


def test_format_submission_date(application_class_data):
    application = application_class_data
    response = application.format_submission_date
    assert response == "14 May 2022 at 10:25am"


def testHealthcheckEndpoint(flask_test_client):
    response = flask_test_client.get("/healthcheck")
    expected_dict = {"check_flask_running": "OK"}
    assert expected_dict in response.json["checks"], "Unexpected json body"
