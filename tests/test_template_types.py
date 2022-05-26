import pytest
from tests.test_magic_link.magic_link_data import incorrect_template_type_key_data # noqa
from tests.test_magic_link.magic_link_data import (incorrect_template_type_value_data) # noqa


@pytest.mark.usefixtures("live_server")
def test_template_type_with_unexpected_key_type(flask_test_client):
    """
    GIVEN: our service running on flask test client.
    WHEN: we post incorrect key "type" to the endpoint
    "/send" using magic_link_data.
    THEN: we check if it returns an error message.
    """

    response = flask_test_client.post(
        "/send",
        json=incorrect_template_type_key_data,
        follow_redirects=True,
    )

    assert (
        b"Incorrect type, please check the key 'type' & other keys, values"
        b" from notification data:"
        in response.data
    )


@pytest.mark.usefixtures("live_server")
def test_template_type_with_unexpected_value_type(flask_test_client):
    """
    GIVEN: our service running on flask test client.
    WHEN: we post unexpected "value" of key "type"
    to the endpoint "/send" using magic_link_data.
    THEN: we check if it returns an error message.
    """

    response = flask_test_client.post(
        "/send",
        json=incorrect_template_type_value_data,
        follow_redirects=True,
    )

    assert (
        b"Incorrect type, please check the key 'type' & other keys, values"
        b" from notification data:"
        in response.data
    )
