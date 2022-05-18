import pytest


@pytest.mark.usefixtures("live_server")
def test_notification_route_response_expected_data(flask_test_client):
    """
    GIVEN: our service running on flask test client.
    WHEN: we post expected data to the endpoint "/send".
    THEN: we expect a successful response 200.
    """

    expected_data = {
        "type": "MAGIC_LINK",
        "to": "test_recipient@email.com",
        "content": {
            "magic_link_url": "MAGIC LINK GOES HERE",
            "fund_name": "FUND NAME GOES HERE",
        },
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
    along with the pre-added template message.
    """

    expected_data = {
        "type": "MAGIC_LINK",
        "to": "test_recipient@email.com",
        "content": {
            "magic_link_url": "MAGIC LINK GOES HERE",
            "fund_name": "FUND NAME GOES HERE",
        },
    }
    response = flask_test_client.post(
        "/send",
        json=expected_data,
        follow_redirects=True,
    )
    assert b"MAGIC LINK GOES HERE" in response.data


@pytest.mark.usefixtures("live_server")
def test_notification_route_response_unexpected_data(flask_test_client):
    """
    GIVEN: our service running on flask test client.
    WHEN: we post unexpected data to the endpoint "/send".
    THEN: we expect a unsuccessful response 400.
    """

    unexpected_data = {
        "te": "MAGIC_LINK",
        "to": "test_recipient@email.com",
        "content": {
            "magic_link_url": "MAGIC LINK GOES HERE",
            "fund_name": "FUND NAME GOES HERE",
        },
    }

    response = flask_test_client.post(
        "/send",
        json=unexpected_data,
        follow_redirects=True,
    )

    assert response.status_code == 400


@pytest.mark.usefixtures("live_server")
def test_notification_contents_unexpected_key_type(flask_test_client):
    """
    GIVEN: our service running on flask test client.
    WHEN: we post incorrect key "type" to the endpoint "/send".
    THEN: we check if it returns an error message.
    """

    unexpected_data = {
        "te": "MAGIC_LINK",
        "to": "test_recipient@email.com",
        "content": {
            "magic_link_url": "MAGIC LINK GOES HERE",
            "fund_name": "FUND NAME GOES HERE",
        },
    }

    response = flask_test_client.post(
        "/send",
        json=unexpected_data,
        follow_redirects=True,
    )

    assert (
        b"Incorrect type, please check the key 'type' & other keys, values"
        b" from notification data:"
        in response.data
    )


@pytest.mark.usefixtures("live_server")
def test_notification_contents_unexpected_value_type(flask_test_client):
    """
    GIVEN: our service running on flask test client.
    WHEN: we post unexpected "value" of key "type" to the endpoint "/send".
    THEN: we check if it returns an error message.
    """

    unexpected_data = {
        "type": "MAGIC_",
        "to": "test_recipient@email.com",
        "content": {
            "magic_link_url": "MAGIC LINK GOES HERE",
            "fund_name": "FUND NAME GOES HERE",
        },
    }

    response = flask_test_client.post(
        "/send",
        json=unexpected_data,
        follow_redirects=True,
    )

    assert (
        b"Incorrect type, please check the key 'type' & other keys, values"
        b" from notification data:"
        in response.data
    )


@pytest.mark.usefixtures("live_server")
def test_notification_contents_incorrect_key(flask_test_client):
    """
    GIVEN: our service running on flask test client.
    WHEN: we post unexpected key to the endpoint "/send".
    THEN: we check if it returns an error message.
    """

    unexpected_data = {
        "type": "MAGIC_LINK",
        "to": "test_recipient@email.com",
        "con": {
            "magic_link_url": "MAGIC LINK GOES HERE",
            "fund_name": "FUND NAME GOES HERE",
        },
    }

    response = flask_test_client.post(
        "/send",
        json=unexpected_data,
        follow_redirects=True,
    )

    assert (
        b"Incorrect data, please check the contents of the notification data."
        in response.data
    )


@pytest.mark.usefixtures("live_server")
def test_notification_contents_multiple_key_errors(flask_test_client):
    """
    GIVEN: our service running on flask test client.
    WHEN: we post incorrect key "type" and other incorrect keys & values
    to the endpoint "/send".
    THEN: we check if it returns an error message.
    """

    unexpected_data = {
        "te": "MAGIC_LINK",
        "t": "test_recipient@email.com",
        "cot": "",
    }

    response = flask_test_client.post(
        "/send",
        json=unexpected_data,
        follow_redirects=True,
    )

    assert (
        b"Incorrect type, please check the key 'type' & other keys, values"
        b" from notification data:"
        in response.data
    )
