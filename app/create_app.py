import connexion

from app.notification.model import read_and_process_from_notify_queue
from flask import Flask
from fsd_utils import init_sentry
from fsd_utils.healthchecks.checkers import FlaskRunningChecker
from apscheduler.schedulers.background import BackgroundScheduler
from fsd_utils.healthchecks.healthcheck import Healthcheck
from fsd_utils.logging import logging


def create_app() -> Flask:
    init_sentry()

    flask_app = Flask(__name__)
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

    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=read_and_process_from_notify_queue,
        trigger="interval",
        seconds=3,  # Every second read from the queue
    )
    scheduler.start()

    try:
        return flask_app
    except Exception:
        return scheduler.shutdown()


app = create_app()
