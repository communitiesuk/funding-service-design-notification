from flask import Flask
from flask_talisman import Talisman
from config import Config
from fsd_utils.logging import logging


def create_app() -> Flask:
    flask_app = Flask("Notification")

    flask_app.config.from_object("config.Config")

    # Initialise logging
    logging.init_app(flask_app)

    # Configure application security with Talisman
    # Talisman(flask_app, **Config.TALISMAN_SETTINGS)

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

    # ---- SETUP BLUEPRINT ROUTES.

    # import notification route.
    from app.notification.model.routes import notification_bp

    # register notification route (blueprint from app/notification/routes).
    flask_app.register_blueprint(notification_bp)

    return flask_app


app = create_app()
