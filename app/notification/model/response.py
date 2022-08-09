from flask import jsonify


def magic_link_error(message: str, code: int = 400):
    return (
        jsonify(
            detail="Incorrect MAGIC LINK data",
            status=code,
            error=f"{message}",
        ),
        code,
    )


def application_submission_error(message: str, code : int = 400):
    return (
        jsonify(
            detail="Incorrect APPLICATION data",
            status=code,
            error=f"{message}",
        ),
        code,
    )

def invalid_email_address_error(message: str, code: int =400):
    return (
        jsonify(
            detail="Not a valid email address",
            status=code,
            error=f"{message}",
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
