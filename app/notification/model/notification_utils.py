import re

from flask import current_app


def convert_bool_value(data):

    try:

        def convert_values(value):
            if value is None:
                return "Not provided"
            elif value is True:
                return "Yes"
            elif value is False:
                return "No"
            else:
                return value

        if isinstance(data, list):
            if all(isinstance(sublist, list) for sublist in data):
                converted_data = [
                    [convert_values(value) for value in sublist]
                    for sublist in data
                ]
            else:
                converted_data = [convert_values(value) for value in data]
        else:
            converted_data = convert_values(data)

        return converted_data
    except Exception as e:
        current_app.logger.error(
            f"Couldn't convert the boolean values: {data}", e
        )
        return data


def format_answer(answer):
    if answer is None:
        return "Not provided"
    if "-" in answer:
        return answer.replace("-", " ")
    if "null" in answer:
        return re.sub(r"\s*null\s*,?", "", answer)

    if isinstance(answer, list):
        return [
            a.replace("'", "").replace("-", " ")
            for a in answer
            if isinstance(a, str)
        ]

    return answer


def simplify_title(section_name, remove_text: list):
    section = section_name.split("-")

    try:
        simplified_title = []

        for i, text in enumerate(section):
            if text in remove_text:
                simplified_title = section[:i]
                break

        if not simplified_title:
            simplified_title = section

        return simplified_title

    except Exception as e:
        current_app.logger.error(
            f"Couldn't simplify the section title{section_name}", e
        )
