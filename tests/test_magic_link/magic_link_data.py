expected_magic_link_data = {
    "type": "MAGIC_LINK",
    "to": "test_recipient@email.com",
    "content": {
        "magic_link_url": "MAGIC LINK GOES HERE",
        "fund_name": "FUND NAME GOES HERE",
    },
}

incorrect_content_key_data = {
    "type": "MAGIC_LINK",
    "to": "test_recipient@email.com",
    "con": {
        "magic_link_url": "MAGIC LINK GOES HERE",
        "fund_name": "FUND NAME GOES HERE",
    },
}

incorrect_template_type_key_data = {
    "te": "MAGIC_LINK",
    "to": "test_recipient@email.com",
    "content": {
        "magic_link_url": "MAGIC LINK GOES HERE",
        "fund_name": "FUND NAME GOES HERE",
    },
}

incorrect_template_type_value_data = {
    "type": "TEST_KEY",
    "to": "test_recipient@email.com",
    "content": {
        "magic_link_url": "CONTENTS GOES HERE",
        "fund_name": "FUND NAME GOES HERE",
    },
}
