import pytest
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

    assert b"Fund name:  Funding service" in response.data


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
    assert b"Application submitted: 2022-05-14" in response.data
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

@pytest.mark.usefixtures("live_server")
def test_application_upload_file_response(flask_test_client):
    """
    GIVEN: our service running on flask test client.
    WHEN: we post expected data with type "file" to endpoint "/send".
    THEN: we check if it returns status code 200.
    """

    response = flask_test_client.post(
        "/send",
        json=expected_application_data,
        follow_redirects=True,
    )
    assert response.status_code == 200

def testHealthcheckEndpoint(flask_test_client):
    response = flask_test_client.get("/healthcheck")
    expected_dict = {"checks": [{"check_flask_running": "OK"}]}
    assert 200 == response.status_code, "Unexpected status code"
    assert expected_dict == response.json, "Unexpected json body"
