import pytest
from tests.test_magic_link.magic_link_data import expected_magic_link_data
from tests.test_magic_link.magic_link_data import incorrect_content_key_data


@pytest.mark.usefixtures("live_server")
def test_magic_link_contents_with_expected_data(flask_test_client):
    """
    GIVEN: our service running on flask test client.
    WHEN: we post expected magic_link_data to the endpoint "/send".
    THEN: we check if the contents of the message is successfully delivered
    along with the pre-added template message.
    """

    response = flask_test_client.post(
        "/send",
        json=expected_magic_link_data,
        follow_redirects=True,
    )
    assert b"MAGIC LINK GOES HERE" in response.data


@pytest.mark.usefixtures("live_server")
def test_magic_link_contents_with_incorrect_content_key(flask_test_client):
    """
    GIVEN: our service running on flask test client.
    WHEN: we post unexpected magic_link_data key to the endpoint "/send".
    THEN: we check if it returns an error message.
    """

    response = flask_test_client.post(
        "/send",
        json=incorrect_content_key_data,
        follow_redirects=True,
    )

    assert (
        b"Incorrect MAGIC LINK data, please check the contents of the MAGIC"
        b" LINK data."
        in response.data
    )


@pytest.mark.usefixtures("live_server")
def test_magic_link_contents_with_none_contents(flask_test_client):
    """
    GIVEN: our service running on flask test client.
    WHEN: we post no data to the endpoint "/send".
    THEN: we check if it returns an error message.
    """

    response = flask_test_client.post(
        "/send",
        json=None,
        follow_redirects=True,
    )

    assert (
        b"Bad request. No data has been received.Please check the contents of"
        b" the notification data:"
        in response.data
    )
