import pytest
from app.notification.application.map_contents import Application
from app.notification.model.notification import Notification
from examplar_data.application_data import (
    expected_application_data,
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


@pytest.mark.usefixtures("live_server")
def test_application_contents_with_formatted_date(flask_test_client):
    """
    GIVEN: our service running on flask test client.
    WHEN: we post expected application data to the endpoint "/send".
    THEN: we check if the contents of the message is successfully delivered
    along with formatted date.
    """

    response = flask_test_client.post(
        "/send",
        json=expected_application_data,
        follow_redirects=True,
    )
    assert b"Application submitted: 14 May 2022 at 10:20am." in response.data
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

    expected_contents_response = (
        b"********* Community Ownership Fund **********\n\n* About your"
        b" org\n\n  Q) Applicant name\n  A) Jack-Simon\n\n  Q) Upload file\n "
        b" A) programmer.jpeg\n\n"
    )

    assert expected_contents_response in questions.getvalue()


def testHealthcheckEndpoint(flask_test_client):
    response = flask_test_client.get("/healthcheck")
    expected_dict = {"checks": [{"check_flask_running": "OK"}]}
    assert 200 == response.status_code, "Unexpected status code"
    assert expected_dict == response.json, "Unexpected json body"
