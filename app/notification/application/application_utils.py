from __future__ import annotations

from app.notification.model.multi_input_data import MultiInput
from bs4 import BeautifulSoup
from flask import current_app
from fsd_utils.config.notify_constants import NotifyConstants


def remove_html_tags(answer):
    """
    Removes HTML tags from the provided answer and returns the cleaned text.

    Args:
        answer (str): The answer containing HTML tags.

    Returns:
        str: The cleaned text with HTML tags removed.
    """

    try:
        if answer is None or isinstance(answer, (bool, list)):
            return answer

        # Check if answer looks like a URL
        if answer.startswith("http://") or answer.startswith("https://"):
            return answer

        soup = BeautifulSoup(answer, "html.parser")
        indent = " " * 5

        if not soup.find():
            return answer.strip()

        if not (soup.ul or soup.ol):
            # Handle other HTML tags
            cleaned_text = soup.get_text()
            cleaned_text = cleaned_text.replace("\xa0", "")
            return cleaned_text.strip()

        soup_list = soup.ul or soup.ol
        list_items = []
        for index, li in enumerate(soup_list.find_all("li"), start=1):
            separator = "-" if soup.ul else f"{index}."
            if li.get_text() == "\xa0":
                continue

            if index > 1:
                list_items.append(f"{indent}{separator} {li.get_text()}")
            else:
                list_items.append(f"{separator} {li.get_text()}")
        return "\n".join(list_items)

    except Exception as e:
        current_app.logger.error(
            f"Error occurred while processing HTML tag: {answer}", e
        )
        return answer


def sort_questions_and_answers(forms, form_names, questions_answers):

    for form_name in form_names:
        try:
            for form in forms:
                if form_name in form[NotifyConstants.APPLICATION_NAME_FIELD]:
                    for question in form[
                        NotifyConstants.APPLICATION_QUESTIONS_FIELD
                    ]:
                        for field in question["fields"]:
                            answer = field.get("answer")
                            clean_html_answer = remove_html_tags(answer)

                            if field["type"] == "file":
                                # we check if the question type is "file"
                                # then we remove the aws
                                # key attached to the answer

                                if isinstance(clean_html_answer, str):
                                    questions_answers[form_name][
                                        field["title"]
                                    ] = clean_html_answer.split("/")[-1]
                                else:
                                    questions_answers[form_name][
                                        field["title"]
                                    ] = clean_html_answer
                            elif (
                                isinstance(clean_html_answer, bool)
                                and field["type"] == "list"
                            ):
                                questions_answers[form_name][
                                    field["title"]
                                ] = ("Yes" if clean_html_answer else "No")
                            elif (
                                isinstance(clean_html_answer, list)
                                and field["type"] == "multiInput"
                            ):

                                questions_answers[form_name][
                                    field["title"]
                                ] = MultiInput.map_multi_input_data(
                                    clean_html_answer
                                )
                            else:
                                questions_answers[form_name][
                                    field["title"]
                                ] = clean_html_answer
        except Exception as e:
            current_app.logger.error(
                f"Error occurred while processing form data: {e}"
            )
            current_app.logger.error(
                f"Could not map the data for form: {form_name}"
            )
    return questions_answers
