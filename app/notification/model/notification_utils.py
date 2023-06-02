import re

from flask import current_app


def convert_bool_value(value):
    return "Yes" if value is True else "No" if value is False else value


def format_answer(answer):
    if answer is None:
        return "Not provided"
    if "-" in answer:
        return answer.replace("-", " ")
    if "null" in answer:
        return re.sub(r"\s*null\s*,?", "", answer)
    return answer
