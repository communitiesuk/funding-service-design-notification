import connexion
from apscheduler.schedulers.background import BackgroundScheduler
from connexion.resolver import MethodViewResolver
from flask import Flask
from fsd_utils import init_sentry
from fsd_utils.healthchecks.checkers import FlaskRunningChecker
from fsd_utils.healthchecks.healthcheck import Healthcheck
from fsd_utils.logging import logging

from app.notification.scheduler.context_aware_executor import ContextAwareExecutor
from app.notification.scheduler.scheduler_service import scheduler_executor
from app.notification.scheduler.task_executer_service import TaskExecutorService
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
            service_meta_description="Funding Service Design Iteration - Notification Hub",
            service_meta_keywords="Funding Service Design - Notification Hub",
            service_meta_author="DLUHC",
        )

    executor = ContextAwareExecutor(
        max_workers=Config.TASK_EXECUTOR_MAX_THREAD, thread_name_prefix="NotifTask", flask_app=flask_app
    )
    # Configure Task Executor service
    task_executor_service = TaskExecutorService(flask_app=flask_app, executor=executor)
    # Configurations for Flask-Apscheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=scheduler_executor,
        trigger="interval",
        seconds=Config.SQS_RECEIVE_MESSAGE_CYCLE_TIME,  # Run the job every 'x' seconds
        kwargs={"task_executor_service": task_executor_service},
    )
    scheduler.start()

    health = Healthcheck(flask_app)
    health.add_check(FlaskRunningChecker())

    return flask_app


app = create_app()
