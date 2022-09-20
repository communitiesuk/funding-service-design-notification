import pytest
from examplar_data.magic_link_data import (incorrect_template_type_data) # noqa
from examplar_data.magic_link_data import incorrect_template_type_key_data # noqa


@pytest.mark.usefixtures("live_server")
def test_template_type_with_unexpected_key_type(flask_test_client):
    """
    GIVEN: our service running on flask test client.
    WHEN: we post incorrect key "type" to the endpoint
    "/send" using magic_link_data.
    THEN: we check if it returns status code 400.
    """

    response = flask_test_client.post(
        "/send",
        json=incorrect_template_type_key_data,
        follow_redirects=True,
    )

    assert response.status_code == 400


@pytest.mark.usefixtures("live_server")
def test_template_type_with_unexpected_value_type(
    flask_test_client, debug=True): # noqa
    """
    GIVEN: our service running on flask test client.
    WHEN: we post unexpected "value" of key "type"
    to the endpoint "/send" using magic_link_data.
    THEN: we check if it returns an error message.
    """

    response = flask_test_client.post(
        "/send",
        json=incorrect_template_type_data,
        follow_redirects=True,
    )
    assert response.status_code == 400
