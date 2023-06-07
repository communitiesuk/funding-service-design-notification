import pytest
from app.notification.model.notification_utils import convert_bool_value
from app.notification.model.notification_utils import format_answer
from app.notification.model.notification_utils import simplify_title


@pytest.mark.parametrize(
    "input_data, expected_response",
    [
        (True, "Yes"),
        (False, "No"),
        (["address", True], ["address", "Yes"]),
        ((["address", False], ["address", "No"])),
        (None, "Not provided"),
        ([["name", True], ["name", "Yes"]]),
        ([["name", False], ["name", "No"]]),
    ],
)
def test_convert_bool_values(app_context, input_data, expected_response):
    response = convert_bool_value(input_data)
    assert response == expected_response


@pytest.mark.parametrize(
    "input_data, expected_response",
    [
        ("null", ""),
        (None, "Not provided"),
    ],
)
def test_format_answer(app_context, input_data, expected_response):
    response = format_answer(input_data)
    assert response == expected_response


@pytest.mark.parametrize(
    "section_name, remove_text, expected_response",
    [
        (
            "organisation-type-cof-round",
            ["cof", "ns"],
            ["organisation", "type"],
        ),
        (
            "organisation-name-ns-round",
            ["cof", "ns"],
            ["organisation", "name"],
        ),
        ("organisation-address", ["cof", "ns"], ["organisation", "address"]),
    ],
)
def test_simplify_title(
    app_context, section_name, remove_text, expected_response
):
    response = simplify_title(section_name, remove_text)
    assert response == expected_response
