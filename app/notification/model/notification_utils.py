import re


def convert_bool_value(data):
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
    simplified_title = []

    section = section_name.split("-")

    for text in remove_text:
        if text in section:
            index = section.index(text)
            simplified_title = [
                item for item in section[:index] if text not in item
            ]
        else:
            simplified_title = section

    return simplified_title
