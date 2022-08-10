from flask import jsonify


def magic_link_key_error(message: str, code: int = 400):
    return (
        jsonify(
            detail="Incorrect MAGIC LINK data",
            status=code,
            error=f"{message}",
        ),
        code,
    )


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
                "Incorrect data, check following contents that may contain"
                " invalid email and incorrect values"
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
