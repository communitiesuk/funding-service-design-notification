import pytest
from tests.test_application_submission.application_data import (
    expected_application_data,
)
from tests.test_application_submission.application_data import (
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
    assert b"List of questions & answers for application" in response.data


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
    assert (
        b"Incorrect APPLICATION data, please check the contents of the"
        b" APPLICATION data"
        in response.data
    )


@pytest.mark.usefixtures("live_server")
def test_application_contents_with_none_contents(flask_test_client):
    """
    GIVEN: our service running on flask test client.
    WHEN: we post no data to the endpoint "/send".
    THEN: we check if it returns an error message.
    """

    response = flask_test_client.post(
        "/send",
        json=None,
        follow_redirects=True,
    )

    assert (
        b"Bad request. No data has been received.Please check the contents of"
        b" the notification data:"
        in response.data
    )
