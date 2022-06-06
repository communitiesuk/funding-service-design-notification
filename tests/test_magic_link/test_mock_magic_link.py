import pytest
from app.notification.model.notifier import Notifier
from app.notification.model.routes import send_email
from tests.test_magic_link.magic_link_data import email_recipient_data
from tests.test_magic_link.magic_link_data import expected_magic_link_data
from tests.test_magic_link.magic_link_data import make_response_data


@pytest.mark.usefixtures("live_server")
@pytest.mark.usefixtures("mocked_magic_link")
def test_mocked_magic_link():

    response_send_email = send_email()
    assert response_send_email == make_response_data
    assert (
        "MAGIC-LINK-GOES-HERE"
        in response_send_email["notify_response"]["content"]["body"]
    )

    response_notify_service = Notifier.send_magic_link(
        expected_magic_link_data
    )
    assert response_notify_service == email_recipient_data
