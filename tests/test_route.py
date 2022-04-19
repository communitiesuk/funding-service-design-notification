from urllib.request import urlopen

import pytest
from app.create_app import create_app
from flask import url_for


@pytest.fixture(scope="session")
def app():
    app = create_app()
    return app


@pytest.mark.usefixtures("live_server")
class TestSearchPage:
    """
    GIVEN class checks if route for send_notification
    is up & running
    """

    def test_notification_route_response(self):
        url = url_for("notification_bp.send_notification", _external=True)
        res = urlopen(url)
        assert res.code == 200


@pytest.fixture()
def flask_test_client():
    """
    Creates the test client we will be using to test the responses
    from our app, this is a test fixture.
    :return: A flask test client.
    """
    with create_app().test_client() as test_client:
        yield test_client


@pytest.mark.usefixtures("live_server")
def test_search_page_found(flask_test_client):
    response = flask_test_client.get(
        url_for("notification_bp.send_notification"),
        follow_redirects=True,
    )
    assert b"content" in response.data
