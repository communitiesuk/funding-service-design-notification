import pytest

from examplar_data.magic_link_data import incorrect_content_body_key


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
        json=incorrect_content_body_key,
        follow_redirects=True,
    )

    assert response.status_code == 400
