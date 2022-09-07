from config import Config

valid_content = {
    Config.NOTIFICATION_MAGIC_LINK_MAGIC_LINK_URL: "MAGIC-LINK-GOES-HERE",
    Config.NOTIFICATION_MAGIC_LINK_FUND_NAME: "FUND NAME GOES HERE",
    Config.NOTIFICATION_MAGIC_LINK_CONTACT_HELP_EMAIL: "HELP EMAIL GOES HERE",
    Config.NOTIFICATION_MAGIC_LINK_REQUEST_NEW_EMAIL_URL: (
        "NEW LINK URL GOES HERE"
    ),
}

expected_magic_link_content = (
    "Key 'content' must contain the required Magic Link data & the data must"
    " be in the JSON format"
)

expected_magic_link_data = {
    "type": "MAGIC_LINK",
    "to": "test_recipient@email.com",
    "content": valid_content,
}

incorrect_content_key_data = {
    "type": "MAGIC_LINK",
    "to": "test_recipient@email.com",
    "con": valid_content,
}

incorrect_template_type_key_data = {
    "te": "MAGIC_LINK",
    "to": "test_recipient@email.com",
    "content": valid_content,
}

incorrect_template_type_data = {
    "type": "TEST_KEY",
    "to": "test_recipient@email.com",
    "content": valid_content,
}


expected_magic_link_response = {
    "notify_response": {
        "content": {
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
