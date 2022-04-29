from urllib.request import urlopen

import pytest
from flask import url_for


@pytest.mark.usefixtures("live_server")
class TestNotificationEndpoint:
    def test_notification_route_response(self):
        """
        GIVEN: our service running on flask test client.
        WHEN: route successfully connects with the send_notification endpoint.
        THEN: we expect a successful response 200.
        """
        url = url_for("notification_bp.send_notification", _external=True)
        res = urlopen(url)
        assert res.code == 200


@pytest.mark.usefixtures("live_server")
def test_notification_successful_content(flask_test_client):
    """
    GIVEN: our service running on flask test client.
    WHEN: we send template to the send_notification
    endpoint/recipient.
    THEN: we checks the content of the message as expected
    if message is delivered successfully.
    """

    response = flask_test_client.get(
        url_for("notification_bp.send_notification"),
        follow_redirects=True,
    )
    assert b"Funding service link" in response.data


@pytest.mark.usefixtures("live_server")
def test_notification_failure_content(flask_test_client):
    """
    GIVEN: our service running on flask test client.
    WHEN: we send template to the send_notification
    endpoint/recipient.
    THEN: we checks if there was any error delivering
    the message to the endpoint.
    """

    response = flask_test_client.get(
        url_for("notification_bp.send_notification"),
        follow_redirects=True,
    )
    assert b"error" not in response.data
