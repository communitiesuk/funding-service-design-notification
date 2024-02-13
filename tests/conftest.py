import multiprocessing
import platform
from unittest.mock import Mock
from unittest.mock import patch

import pytest
from app.create_app import create_app
from app.notification.application.map_contents import Application
from examplar_data.application_data import expected_application_response
from examplar_data.magic_link_data import expected_magic_link_response
from flask import Request
from notifications_python_client import NotificationsAPIClient


if platform.system() == "Darwin":
    multiprocessing.set_start_method("fork")  # Required on macOSX


@pytest.fixture()
def flask_test_client():
    """
    Creates the test client we will be using to test the responses
    from our app, this is a test fixture.
    :return: A flask test client.
    """
    with create_app().test_client() as test_client:
        yield test_client


@pytest.fixture(scope="session")
def app():
    app = create_app()
    return app


@pytest.fixture()
def app_context():
    """
    Creates both the app context and the request context as a single fixture.
    """
    app = create_app()

    with app.app_context(), app.test_request_context():
        yield app


@pytest.fixture(autouse=False)
def mock_application_class_data():
    return Application(
        contact_info="example@example.com",
        contact_name="Test User",
        questions=b"",
        fund_name="Example Fund",
        round_name="Round 1",
        reference="ABC123",
        submission_date="2022-05-14T09:25:44.124542",
        fund_id="test_fund_id",
        reply_to_email_id="test_email_address",
    )


@pytest.fixture(autouse=False)
def mock_request_data(mocker, content_available=True):
    mock_data = {
        "content": {
            "contact_help_email": "nope@wrong.gov.uk",
            "fund_name": "FUND NAME GOES HERE",
            "magic_link_url": "MAGIC-LINK-GOES-HERE",
            "request_new_link_url": "NEW LINK URL GOES HERE",
        },
        "to": "test_recipient@email.com",
        "type": "MAGIC_LINK",
    }

    mocker.patch.object(Request, "get_json", return_value=mock_data)
    return mock_data


@pytest.fixture(autouse=False)
def mock_notify_response(mocker, request, mock_request_data):
    if request.param == "empty_content":
        request_data = {"content": ""}
    else:
        request_data = mock_request_data

    status_code = 200 if request_data["content"] else 400
    response_data = (
        {"success": True}
        if status_code == 200
        else {"error": "Invalid request"}
    )
    response = (response_data, status_code)
    mocker.patch(
        "app.notification.model.Notification.email_recipient",
        return_value=response,
    )
    return response


@pytest.fixture
def mock_notifications_api_client(request):
    mock_data = request.param

    if mock_data == 1:
        mock_data = (
            expected_magic_link_response  # EXPECTED DATA FOR MAGIC LINK
        )
    elif mock_data == 2:
        mock_data = (
            expected_application_response  # EXPECTED DATA FOR APPLICATION
        )

    notifications_client = Mock(spec=NotificationsAPIClient)
    notifications_client.send_email_notification.return_value = (
        mock_data,
        200,
    )
    return notifications_client


@pytest.fixture
def mock_notifier_api_client(mock_notifications_api_client):
    mock_api_key = "MOCK_API_KEY"  # pragma: allowlist secret
    with patch(
        "app.notification.model.notifier.NotificationsAPIClient",
        return_value=mock_notifications_api_client,
    ):
        with patch(
            "app.notification.model.notifier.Config.GOV_NOTIFY_API_KEY",
            mock_api_key,
        ):
            yield
