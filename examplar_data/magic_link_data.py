from fsd_utils.config.notify_constants import NotifyConstants

valid_content = {
    NotifyConstants.MAGIC_LINK_URL_FIELD: "MAGIC-LINK-GOES-HERE",
    NotifyConstants.MAGIC_LINK_FUND_NAME_FIELD: "FUND NAME GOES HERE",
    NotifyConstants.MAGIC_LINK_CONTACT_HELP_EMAIL_FIELD: (
        "COF@levellingup.gov.uk"
    ),
    NotifyConstants.MAGIC_LINK_REQUEST_NEW_LINK_URL_FIELD: (
        "NEW LINK URL GOES HERE"
    ),
}

not_valid_content = {
    NotifyConstants.MAGIC_LINK_URL_FIELD: "MAGIC-LINK-GOES-HERE",
    NotifyConstants.MAGIC_LINK_FUND_NAME_FIELD: "FUND NAME GOES HERE",
    NotifyConstants.MAGIC_LINK_CONTACT_HELP_EMAIL_FIELD: "nope@wrong.gov.uk",
    NotifyConstants.MAGIC_LINK_REQUEST_NEW_LINK_URL_FIELD: (
        "NEW LINK URL GOES HERE"
    ),
}

expected_magic_link_content = (
    "Key 'content' must contain the required Magic Link data & the data must"
    " be in the JSON format"
)

expected_magic_link_data = {
    NotifyConstants.FIELD_TYPE: "MAGIC_LINK",
    NotifyConstants.FIELD_TO: "test_recipient@email.com",
    NotifyConstants.FIELD_CONTENT: valid_content,
}

expected_magic_link_unknown_help_email = {
    NotifyConstants.FIELD_TYPE: "MAGIC_LINK",
    NotifyConstants.FIELD_TO: "test_recipient@email.com",
    NotifyConstants.FIELD_CONTENT: not_valid_content,
}

incorrect_content_key_data = {
    NotifyConstants.FIELD_TYPE: "MAGIC_LINK",
    NotifyConstants.FIELD_TO: "test_recipient@email.com",
    "con": valid_content,
}

incorrect_template_type_key_data = {
    "te": "MAGIC_LINK",
    NotifyConstants.FIELD_TO: "test_recipient@email.com",
    NotifyConstants.FIELD_CONTENT: valid_content,
}

incorrect_template_type_data = {
    NotifyConstants.FIELD_TYPE: "TEST_KEY",
    NotifyConstants.FIELD_TO: "test_magic_link@example.com",
    NotifyConstants.FIELD_CONTENT: valid_content,
}


expected_magic_link_response = {
    "notify_response": {
        NotifyConstants.FIELD_CONTENT: {
            "body": (
                "You asked us for a link to your application:  \r\nMAGIC-LINK-"
                "GOES-HERE \r\n\r\nThe link will work for 24 hours."
                " \r\n\r\n\r\nFUND NAME GOES HERE\r\n---\r\nThis is an"
                " automated message. Do not reply to this email. If you need"
                " help, contact dummy_contact_info@funding-service-help.com."
            ),
            "from_email": "test_sender@email.com",
            "subject": "Access your application for the FUND NAME GOES HERE",
        },
        "id": "1234567890-a",
        "reference": None,
        "scheduled_for": None,
        "template": {
            "id": "1234567890-b",
            "uri": "https://test.api.notification.co.uk/services/1234567890-c",  # noqa
            "version": 29,
        },
        "uri": "https://test.api.notification.co.uk/v2/notifications/",  # noqa
    },
    "status": "ok",
}


def expected_magic_link_data():
    return {
        "content": {
            "body": "You requested a link to start or continue an application"
        },
        "id": "431ff6c3",
        "reference": None,
        "scheduled_for": None,
        "template": {
            "id": "02a6d48a",
            "uri": "https://api.com/",
            "version": 11,
        },
        "uri": "https://api.com",
    }
