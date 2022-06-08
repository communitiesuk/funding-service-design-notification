import pytest
from tests.test_magic_link.magic_link_data import expected_magic_link_data
from tests.test_magic_link.magic_link_data import incorrect_content_key_data


@pytest.mark.usefixtures("live_server")
def test_send_email_route_response_with_expected_data(flask_test_client):
    """
    GIVEN: our service running on flask test client.
    WHEN: we post expected data to the endpoint "/send using magic_link_data".
    THEN: we expect a successful response 200.
    """

    response = flask_test_client.post(
        "/send",
        json=expected_magic_link_data,
        follow_redirects=True,
    )
    assert response.status_code == 200


@pytest.mark.usefixtures("live_server")
def test_send_email_route_response_with_unexpected_data(flask_test_client):
    """
    GIVEN: our service running on flask test client.
    WHEN: we post unexpected data to the endpoint "/send
    using magic_link_data".
    THEN: we expect a unsuccessful response 400.
    """

    response = flask_test_client.post(
        "/send",
        json=incorrect_content_key_data,
        follow_redirects=True,
    )

    assert response.status_code == 400
