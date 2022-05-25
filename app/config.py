"""Flask configuration."""
import os

SECRET_KEY = os.environ.get("SECRET_KEY") or "dev"
SESSION_COOKIE_NAME = os.environ.get("SESSION_COOKIE_NAME") or "session_cookie"
STATIC_FOLDER = "static"
TEMPLATES_FOLDER = "templates"
FLASK_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
FLASK_ENV = os.environ.get("FLASK_ENV")

# CURRENTLY TEST KEY IS BEING USED LOCALLY & ON CF.
API_KEY = os.environ.get("GOV_NOTIFY_API_KEY") or os.environ.get(
    "TEST_API_KEY"
)

MAGIC_LINK_TEMPLATE_ID = "02a6d48a-f227-4b9a-9dd7-9e0cf203c8a2"
APPLICATION_RECORD_TEMPLATE_ID = "0ddadcb3-ebe7-44f9-90e6-80ff3b61e0cb"
