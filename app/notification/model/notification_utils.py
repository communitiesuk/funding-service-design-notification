import re


def convert_bool_value(value):
    if value is None:
        return "Not provided"
    else:
        return [
            "Yes" if v is True else "No" if v is False else v for v in value
        ]


def format_answer(answer):
    if answer is None:
        return "Not provided"
    if "-" in answer:
        return answer.replace("-", " ")
    if "null" in answer:
        return re.sub(r"\s*null\s*,?", "", answer)
    return answer
