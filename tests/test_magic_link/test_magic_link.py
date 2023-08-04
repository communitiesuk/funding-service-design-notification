import pytest
from app.notification.model.notifier import Notifier
from examplar_data.magic_link_data import (
    expected_magic_link_unknown_help_email,
)
from examplar_data.magic_link_data import incorrect_content_key_data
from tests.conftest import expected_magic_link_data


@pytest.mark.usefixtures("live_server")
def test_magic_link_contents_with_incorrect_content_key(flask_test_client):
    """
    GIVEN: our service running on flask test client.
    WHEN: we post unexpected magic_link_data key to the endpoint "/send".
    THEN: we check if it returns status code 400.
    """

    response = flask_test_client.post(
        "/send",
        json=incorrect_content_key_data,
        follow_redirects=True,
    )

    assert response.status_code == 400


@pytest.mark.usefixtures("live_server")
def test_magic_link_contents_with_unknown_contact_email(flask_test_client):
    """
    GIVEN: our service running on flask test client.
    WHEN: we post unexpected magic_link_data key to the endpoint "/send".
    THEN: we check if it returns status code 400.
    """

    response = flask_test_client.post(
        "/send",
        json=expected_magic_link_unknown_help_email,
        follow_redirects=True,
    )

    assert response.status_code == 400


@pytest.mark.usefixtures("live_server")
def test_magic_link_contents_with_none_contents(flask_test_client):
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


@pytest.mark.parametrize(
    "mock_notifications_api_client",
    [1],
    indirect=True,
)
def test_send_magic_link(
    app_context,
    mock_notifier_api_client,
    mock_notification_class_data_for_magic_link,
    mock_notifications_api_client,
):

    response, code = Notifier.send_magic_link(
        mock_notification_class_data_for_magic_link, code=200
    )

    assert response == (expected_magic_link_data(), code)
