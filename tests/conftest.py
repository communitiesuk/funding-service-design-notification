import multiprocessing
import platform

import pytest
from app.create_app import create_app
from app.notification.application.map_contents import Application


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
    with create_app().app_context():
        yield


@pytest.fixture(autouse=False)
def application_class_data():
    return Application(
        contact_info="example@example.com",
        questions=b"",
        fund_name="Example Fund",
        round_name="Round 1",
        reference="ABC123",
        submission_date="2022-05-14T09:25:44.124542",
        fund_id="test_fund_id",
        reply_to_email_id="test_email_address",
    )
