from flask import jsonify


def magic_link_error(message):
    return (
        jsonify(
            detail="Incorrect MAGIC LINK data",
            status=400,
            expected_data=f"{message}",
        ),
        400,
    )


def application_submission_error(message):
    return (
        jsonify(
            detail="Incorrect APPLICATION data",
            status=400,
            expected_data=f"{message}",
        ),
        400,
    )


def template_type_error(message):
    return (
        jsonify(
            detail=(
                "Incorrect type, please check the value of key 'type':"
                f" {message.get('type')}"
            ),
            status=400,
            expected_type=(
                "MAGIC_LINK",
                "NOTIFICATION",
                "REMINDER",
                "AWARD",
                "APPLICATION_RECORD_OF_SUBMISSION",
            ),
        ),
        400,
    )
