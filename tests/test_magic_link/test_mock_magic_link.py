import pytest
from app.notification.model import send_email


@pytest.mark.usefixtures("live_server")
@pytest.mark.usefixtures("mocked_magic_link")
def test_mocked_magic_link():
    """
    GIVEN: our service running on unittest mock & pytest-mock library.
    WHEN: (a) we mock expected magic_link json & response contents.
        : (b) we make a call to "send_email()" function.
    THEN: (a) we check  "send_email()" returns the
        expected mocked contents.
    """

    send_email_route_response = send_email()
    assert (
        "MAGIC-LINK-GOES-HERE" in send_email_route_response[0][0]["content"]["body"]
    )
