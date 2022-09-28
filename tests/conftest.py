import multiprocessing
import platform

import pytest
from app.create_app import create_app


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
