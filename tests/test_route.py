from urllib.request import urlopen

import pytest
from flask import url_for


@pytest.mark.usefixtures("live_server")
class TestNotificationEndpoint:
    def test_notification_route_response(self):
        """
        GIVEN: function runs to connect with send_notification route/endpoint.
        WHEN: function successfully connects with the endpoint.
        THEN: function check the response 200(successful) in return.
       """
        url = url_for("notification_bp.send_notification", _external=True)
        res = urlopen(url)
        assert res.code == 200


@pytest.mark.usefixtures("live_server")
def test_notification_successful_content(flask_test_client):
    """
    GIVEN: function sends template to send_notification route/endpoint.
    WHEN: template/message is successfully delivered to the endpoint/recipient.
    THEN: function checks the content of the message delivered as expected.
    """

    response = flask_test_client.get(
        url_for("notification_bp.send_notification"),
        follow_redirects=True,
    )
    assert b"Service-is-being-tested" in response.data

 
@pytest.mark.usefixtures("live_server")
def test_notification_failure_content(flask_test_client):
    """
    GIVEN: function sends template to send_notification route/endpoint.
    WHEN: template/message is delivered to the endpoint/recipient.
    THEN: function checks if there was any error message while delivering
    template/message.
    """
    
    response = flask_test_client.get(
        url_for("notification_bp.send_notification"),
        follow_redirects=True,
    )
    assert b"error" not in response.data
