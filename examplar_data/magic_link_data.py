from app.notification.model.notification import Notification
from fsd_utils.config.notify_constants import NotifyConstants

valid_content_body = {
    NotifyConstants.MAGIC_LINK_URL_FIELD: "MAGIC-LINK-GOES-HERE",
    NotifyConstants.MAGIC_LINK_FUND_NAME_FIELD: "FUND NAME GOES HERE",
    NotifyConstants.MAGIC_LINK_CONTACT_HELP_EMAIL_FIELD: ("COF@levellingup.gov.uk"),
    NotifyConstants.MAGIC_LINK_REQUEST_NEW_LINK_URL_FIELD: ("NEW LINK URL GOES HERE"),
}

invalid_content_body = {
    NotifyConstants.MAGIC_LINK_URL_FIELD: "MAGIC-LINK-GOES-HERE",
    NotifyConstants.MAGIC_LINK_FUND_NAME_FIELD: "FUND NAME GOES HERE",
    NotifyConstants.MAGIC_LINK_CONTACT_HELP_EMAIL_FIELD: "nope@wrong.gov.uk",
    NotifyConstants.MAGIC_LINK_REQUEST_NEW_LINK_URL_FIELD: ("NEW LINK URL GOES HERE"),
}

expected_magic_link_unknown_help_email = {
    NotifyConstants.FIELD_TYPE: "MAGIC_LINK",
    NotifyConstants.FIELD_TO: "test_recipient@email.com",
    NotifyConstants.FIELD_CONTENT: invalid_content_body,
}

incorrect_content_body_key = {
    NotifyConstants.FIELD_TYPE: "MAGIC_LINK",
    NotifyConstants.FIELD_TO: "test_recipient@email.com",
    "con": valid_content_body,
}

incorrect_template_type_key = {
    "te": "MAGIC_LINK",
    NotifyConstants.FIELD_TO: "test_recipient@email.com",
    NotifyConstants.FIELD_CONTENT: valid_content_body,
}

incorrect_template_type = {
    NotifyConstants.FIELD_TYPE: "TEST_KEY",
    NotifyConstants.FIELD_TO: "test_magic_link@example.com",
    NotifyConstants.FIELD_CONTENT: valid_content_body,
}

expected_magic_link_response = {
    "content": {"body": "You requested a link to start or continue an application"},
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


def notification_class_data_for_magic_link():
    return Notification(
        template_type="MAGIC_LINK",
        contact_info="testing_magic_link@example.com",
        contact_name="Test User",
        content={
            "contact_help_email": "nope@wrong.gov.uk",
            "fund_name": "Funding service",
            "magic_link_url": "https://www.example.com/",
            "request_new_link_url": "https://www.example.com/new_link",
        },
    )
