from flask import jsonify


def invalid_data_error(
    message: dict,
    code: int = 400,
):
    return (
        jsonify(
            detail=(
                "Incorrect data, check following contents that may contain"
                " invalid email and incorrect or null values"
            ),
            status=code,
            error=message,
        ),
        code,
    )


def template_type_error(message: str, code: int = 400):
    return (
        jsonify(
            detail=("Incorrect template type, please check the template type:" f" {message.get('type')}"),
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
