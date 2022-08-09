from flask import jsonify


def magic_link_error(email, fund_name, magic_link_url):
    return {
        "email_address": email,
        "fund_name": fund_name,
        "magic_link": magic_link_url,
    }


def magic_link_key_error(message: str, code: int = 400):
    return (
        jsonify(
            detail="Incorrect MAGIC LINK data",
            status=code,
            error=f"{message}",
        ),
        code,
    )


def application_error(
    email, fund_name, application_id, date_submitted, round_name, questions
):
    return {
        "email_address": email,
        "fund_name": fund_name,
        "application_id": application_id,
        "date_submitted": date_submitted,
        "round_name": round_name,
        "questions": questions,
    }


def application_key_error(message: str, code: int = 400):
    return (
        jsonify(
            detail="Incorrect or missing APPLICATION data",
            status=code,
            error=f"{message}",
        ),
        code,
    )


def invalid_data_error(
    message: dict,
    code: int = 400,
):
    return (
        jsonify(
            detail=(
                "Please check following data that may contain invalid email"
                " and incorrect data"
            ),
            status=code,
            error=message,
        ),
        code,
    )


def template_type_error(message: str, code: int = 400):
    return (
        jsonify(
            detail=(
                "Incorrect type, please check the value of key 'type':"
                f" {message.get('type')}"
            ),
            status=code,
            expected_type=(
                "MAGIC_LINK",
                "NOTIFICATION",
                "REMINDER",
                "AWARD",
                "APPLICATION_RECORD_OF_SUBMISSION",
            ),
        ),
        code,
    )


def invalid_email_address_error(message: str, code: int = 400):
    return (
        jsonify(
            detail="Not a valid email address",
            status=code,
            error=f"{message}",
        ),
        code,
    )
