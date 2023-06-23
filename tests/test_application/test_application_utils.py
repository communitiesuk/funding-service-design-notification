import collections

import pytest
from app.notification.application.application_utils import remove_html_tags
from app.notification.application.application_utils import (
    sort_questions_and_answers,
)
from app.notification.model.notification_utils import format_checkbox
from examplar_data.application_data import test_data_sort_questions_answers


@pytest.mark.parametrize(
    "input_value, expected_response",
    [
        ("<p> Hello world </p>", "Hello world"),
        ("<ul><li>Item 1</li><li>Item 2</li></ul>", ". Item 1\n     . Item 2"),
        (
            "<ol><li>Item 1</li><li>Item 2</li></ol>",
            "1. Item 1\n     2. Item 2",
        ),
        ("text without html tags", "text without html tags"),
        (None, None),
        (["one", "two"], ["one", "two"]),
        (True, True),
        ("https://my-website.com", "https://my-website.com"),
    ],
)
def test_remove_html_tags(app_context, input_value, expected_response):

    response = remove_html_tags(input_value)
    assert response == expected_response


def test_sort_questions_and_answers(app_context):
    forms = test_data_sort_questions_answers["forms"]
    form_names = test_data_sort_questions_answers["form_names"]

    response = sort_questions_and_answers(
        forms, form_names, questions_answers=collections.defaultdict(dict)
    )

    assert response == test_data_sort_questions_answers["questions_answers"]


def test_sort_questions_and_answers_fail(app_context):
    forms = test_data_sort_questions_answers["incorrect_form_data"]
    form_names = test_data_sort_questions_answers["form_names"]

    with pytest.raises(Exception) as exc:
        sort_questions_and_answers(
            forms, form_names, questions_answers=collections.defaultdict(dict)
        )

    assert (
        str(exc.value) == test_data_sort_questions_answers["exception_message"]
    )


@pytest.mark.parametrize(
    "input_value, expected_response",
    [
        (
            [
                "health-interventions",
                "employment-support",
            ],
            "- health interventions\n     - employment support",
        ),
        (
            ["Survivors of domestic abuse", "ethnic minorities"],
            "- Survivors of domestic abuse\n     - ethnic minorities",
        ),
    ],
)
def test_format_checkbox(app_context, input_value, expected_response):

    response = format_checkbox(input_value)
    assert response == expected_response
