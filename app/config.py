"""Flask configuration."""
import os


SESSION_COOKIE_NAME = os.environ.get("SESSION_COOKIE_NAME") or "session_cookie"
STATIC_FOLDER = "static"
TEMPLATES_FOLDER = "templates"
FLASK_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
FLASK_ENV = os.environ.get("FLASK_ENV")

API_KEY = os.environ.get("GOV_NOTIFY_API_KEY") or os.environ.get(
    "TEST_API_KEY"
)
TEMPLATE_ID = os.environ.get("GOV_NOTIFY_TEMPLATE_KEY") or os.environ.get(
    "TEST_TEMPLATE_ID"
)
EMAIL_ADDRESS = os.environ.get(
    "GOV_NOTIFY_DEFAULT_EMAIL_ADDRESS"
) or os.environ.get("TEST_EMAIL_ADDRESS")

print(EMAIL_ADDRESS)
