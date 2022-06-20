import os

from flask import Flask
from flask_compress import Compress
from flask_talisman import Talisman


def create_app(testing=False) -> Flask:

    # ---- SETUP STATIC URL PATH.
    flask_app = Flask(__name__)

    # If testing or in dev print current config
    if (os.environ.get("FLASK_ENV") == "development") | testing:
        flask_app.config.from_object("config.development.DevelopmentConfig")
        from config.development import DevelopmentConfig

        DevelopmentConfig.pretty_print()
    else:
        flask_app.config.from_object("config.default.DefaultConfig")

    # ---- SETUP SECURITY CONFIGURATION & CSRF PROTECTION.
    csp = {
        "default-src": "'self'",
        "script-src": [
            "'self'",
            "'sha256-+6WnXIl4mbFTCARd8N3COQmT3bJJmo32N8q8ZSQAIcU='",
            "'sha256-l1eTVSK8DTnK8+yloud7wZUqFrI0atVo6VlC6PJvYaQ='",
        ],
        "img-src": ["data:", "'self'"],
    }

    hss = {
        "Strict-Transport-Security": (
            "max-age=31536000; includeSubDomains; preload"
        ),
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "SAMEORIGIN",
        "X-XSS-Protection": "1; mode=block",
        "Feature_Policy": (
            "microphone 'none'; camera 'none'; geolocation 'none'"
        ),
    }

    Compress(flask_app)
    Talisman(
        flask_app,
        content_security_policy=csp,
        strict_transport_security=hss,
        force_https=False,
    )

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
