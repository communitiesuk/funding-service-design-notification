import connexion
from connexion.resolver import MethodViewResolver
from flask import Flask
from fsd_utils import init_sentry
from fsd_utils.healthchecks.checkers import FlaskRunningChecker
from fsd_utils.healthchecks.healthcheck import Healthcheck
from fsd_utils.logging import logging

from config import Config
from openapi.utils import get_bundled_specs


def create_app() -> Flask:
    init_sentry()

    connexion_options = {"swagger_url": "/"}
    connexion_app = connexion.FlaskApp(
        __name__,
        specification_dir=Config.FLASK_ROOT + "/openapi/",
        options=connexion_options,
    )
    connexion_app.add_api(
        get_bundled_specs("/openapi/api.yml"),
        validate_responses=True,
        resolver=MethodViewResolver("api"),
    )

    # Configure Flask App
    flask_app = connexion_app.app
    flask_app.config.from_object("config.Config")

    # Initialise logging
    logging.init_app(flask_app)

    # ---- SETUP GLOBAL CONSTANTS (to be accessed from the app).
    @flask_app.context_processor
    def inject_global_constants():
        return dict(
            stage="beta",
            service_title="Funding Service Design - Notification Hub",
            service_meta_description=(
                "Funding Service Design Iteration - Notification Hub"
            ),
            service_meta_keywords="Funding Service Design - Notification Hub",
            service_meta_author="DLUHC",
        )

    health = Healthcheck(flask_app)
    health.add_check(FlaskRunningChecker())

    return flask_app


app = create_app()
