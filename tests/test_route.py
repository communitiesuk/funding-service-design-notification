import pytest


@pytest.mark.usefixtures("live_server")
def test_notification_route_response_expected_data(flask_test_client):
    """
    GIVEN: our service running on flask test client.
    WHEN: we post expected data to the endpoint "/send".
    THEN: we expect a successful response 200.
    """

    expected_data = {
        "type": "TEST_MAGIC_LINK",
        "to": "test_recipient@email.com",
        "content": "MAGIC LINK GOES HERE",
    }
    response = flask_test_client.post(
        "/send",
        json=expected_data,
        follow_redirects=True,
    )
    assert response.status_code == 200


@pytest.mark.usefixtures("live_server")
def test_notification_contents_expected_data(flask_test_client):
    """
    GIVEN: our service running on flask test client.
    WHEN: we post expected data to the endpoint "/send".
    THEN: we check if the contents of the message is successfully delivered
    along with the pre-added template message
     ("Click on the link to access your account:  ")
    """

    expected_data = {
        "type": "TEST_MAGIC_LINK",
        "to": "test_recipient@email.com",
        "content": "MAGIC LINK GOES HERE",
    }
    response = flask_test_client.post(
        "/send",
        json=expected_data,
        follow_redirects=True,
    )
    response_data = response.get_json()
    assert (
        response_data["content"]["body"]
        == "Click on the link to access your account:  MAGIC LINK GOES HERE"
    )


@pytest.mark.usefixtures("live_server")
def test_notification_route_response_unexpected_data(flask_test_client):
    """
    GIVEN: our service running on flask test client.
    WHEN: we post unexpected data to the endpoint "/send".
    THEN: we expect a successful response 200.
    """

    unexpected_data = {
        "tpe": "TEST_MAGIC_LINK",
        "to": "test_recipient@email.com",
        "content": "MAGIC LINK GOES HERE",
    }

    response = flask_test_client.post(
        "/send",
        json=unexpected_data,
        follow_redirects=True,
    )

    assert response.status_code == 200


@pytest.mark.usefixtures("live_server")
def test_notification_contents_unexpected_data(flask_test_client):
    """
    GIVEN: our service running on flask test client.
    WHEN: we post unexpected data to the endpoint "/send".
    THEN: we check if the contents of the message are not delivered &
    returns an error message includes
    ("Bad request, please check the contents of the notification data:")
    """

    unexpected_data = {
        "tpe": "TEST_MAGIC_LINK",
        "to": "test_recipient@email.com",
        "content": "MAGIC LINK GOES HERE",
    }

    response = flask_test_client.post(
        "/send",
        json=unexpected_data,
        follow_redirects=True,
    )

    assert (
        b"Bad request, please check the contents of the notification data:"
        in response.data
    )
