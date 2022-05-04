"""Flask configuration."""
import os

SECRET_KEY = os.environ.get("SECRET_KEY") or "dev"
SESSION_COOKIE_NAME = os.environ.get("SESSION_COOKIE_NAME") or "session_cookie"
STATIC_FOLDER = "static"
TEMPLATES_FOLDER = "templates"
FLASK_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
FLASK_ENV = os.environ.get("FLASK_ENV")

# CURRENTLY TEST KEY IS BEING USED LOCALLY & ON CF TO TEST THE SERVICE
API_KEY = os.environ.get("GOV_NOTIFY_API_KEY") or os.environ.get(
    "TEST_API_KEY"
)

# UPDATED GOV_NOTIFY_TEMPLATE_KEY WITH TEST_MAGIC_LINK_TEMPLATE_ID
TEMPLATE_ID = os.environ.get("GOV_NOTIFY_TEMPLATE_KEY") or os.environ.get(
    "TEST_MAGIC_LINK_TEMPLATE_ID"
)


# TO BE REMOVED (NOT IN USE)
EMAIL_ADDRESS = os.environ.get(
    "GOV_NOTIFY_DEFAULT_EMAIL_ADDRESS"
) or os.environ.get("TEST_EMAIL_ADDRESS")
