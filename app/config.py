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

# CURRENTLY TEST_MAGIC_LINK_TEMPLATE_ID IS BEING USED LOCALLY & ON CF.
MAGIC_LINK_TEMPLATE_ID = os.environ.get(
    "GOV_NOTIFY_TEMPLATE_KEY"
) or os.environ.get("TEST_MAGIC_LINK_TEMPLATE_ID")

APPLICATION_RECORD_TEMPLATE_ID = os.environ.get(
    "GOV_NOTIFY_APPLICATION_RECORD_TEMPLATE_KEY"
) or os.environ.get("APPLICATION_RECORD_TEMPLATE_ID")
