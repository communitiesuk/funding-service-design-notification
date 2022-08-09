import pytest
from app.create_app import create_app
from tests.test_application.application_data import expected_application_data
from tests.test_application.application_data import (
    expected_application_response,
)
from tests.test_magic_link.magic_link_data import expected_magic_link_data
from tests.test_magic_link.magic_link_data import expected_magic_link_response


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
def mocked_magic_link(mocker):
    mocker.patch(
        "app.notification.model.request.get_json",
        return_value=expected_magic_link_data,
    )

    mocker.patch(
        "app.notification.model.template_types.email_recipient",
        return_value=expected_magic_link_response,
    )


@pytest.fixture()
def mocked_application(mocker):
    mocker.patch(
        "app.notification.model.request.get_json",
        return_value=expected_application_data,
    )

    mocker.patch(
        "app.notification.model.template_types.email_recipient",
        return_value=expected_application_response,
    )
