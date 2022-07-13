import pytest
from app.notification.model import send_email


@pytest.mark.usefixtures("live_server")
@pytest.mark.usefixtures("mocked_application")
def test_mocked_application():
    """
    GIVEN: our service running on unittest mock & pytest-mock library.
    WHEN: (a) we mock expected application json & response contents.
        : (b) we make a call to "send_email()" function.
    THEN: (a) we check  "send_email()" returns the
        expected mocked contents.
    """

    send_email_route_response = send_email()
    assert "Jack-Simon" in send_email_route_response["content"]["body"]
