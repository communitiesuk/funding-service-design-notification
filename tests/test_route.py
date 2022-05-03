import json

import pytest
from flask import url_for


@pytest.mark.usefixtures("live_server")
def test_notification_route_response(flask_test_client):
    """
    GIVEN: our service running on flask test client.
    WHEN: route successfully connects with the send_notification endpoint.
    THEN: we expect a successful response 200.
    """

    response = flask_test_client.post(
        url_for("notification_bp.send_notification"),
        follow_redirects=True,
    )
    assert response.status_code == 200


@pytest.mark.usefixtures("live_server")
def test_notification_successful_content(flask_test_client):
    """
    GIVEN: our service running on flask test client.
    WHEN: we send template to the send_notification
    endpoint/recipient.
    THEN: we checks the subject content of the message as expected
    to make sure message is delivered successfully.
    """
    data = {
        "type": "TEST_MAGIC_LINK",
        "to": "test_recipient@email.com",
        "content": "MAGIC LINK GOES HERE",
    }

    response = flask_test_client.post(
        url_for("notification_bp.send_notification", data=json.dumps(data)),
        follow_redirects=True,
    )

    assert b"MAGIC LINK GOES HERE" in response.data


@pytest.mark.usefixtures("live_server")
def test_notification(flask_test_client):

    data = {
        "type": "TEST_MAGIC_LINK",
        "to": "test_recipient@email.com",
        "content": "MAGIC LINK GOES HERE",
    }

    response = flask_test_client.post("/send", json=data)
    assert response.status_code == 200


@pytest.mark.usefixtures("live_server")
def test_notification_failure_content(flask_test_client):
    """
    GIVEN: our service running on flask test client.
    WHEN: we send template to the send_notification
    endpoint/recipient.
    THEN: we checks if there was any error delivering
    the message to the endpoint/recipient.
    """

    response = flask_test_client.post(
        url_for("notification_bp.send_notification"),
        follow_redirects=True,
    )
    assert b"error" not in response.data
