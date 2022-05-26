"""Flask configuration."""
import os

FLASK_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
FLASK_ENV = os.environ.get("FLASK_ENV")

# CURRENTLY TEST API KEY IS BEING USED LOCALLY & ON CF.
API_KEY = os.environ.get("GOV_NOTIFY_API_KEY") or os.environ.get(
    "TEST_API_KEY"
)

MAGIC_LINK_TEMPLATE_ID = "02a6d48a-f227-4b9a-9dd7-9e0cf203c8a2"
APPLICATION_RECORD_TEMPLATE_ID = "0ddadcb3-ebe7-44f9-90e6-80ff3b61e0cb"
