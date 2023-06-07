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
        current_app.logger.error(f"Could not convert boolean values, {e}")
        


def format_answer(answer):
    try:
        if answer is None:
            return "Not provided"

        if "null" in answer:
            return re.sub(r"\s*null\s*,?", "", answer)

        if isinstance(answer, list):
            return [a.replace("'", "") for a in answer if isinstance(a, str)]

        return answer
    except Exception as e:
        current_app.logger.error(f"Could not format the answer, {e}")


def simplify_title(section_name, remove_text: list):
    try:
        section = section_name.split("-")
        simplified_title = []

        for i, text in enumerate(section):
            if text in remove_text:
                simplified_title = section[:i]
                break

        if not simplified_title:
            simplified_title = section

        return simplified_title
    except Exception as e:
        current_app.logger.error(f"Could not simplify the section title, {e}")
