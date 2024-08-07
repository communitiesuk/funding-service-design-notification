import connexion
from apscheduler.schedulers.background import BackgroundScheduler
from connexion import FlaskApp
from connexion.resolver import MethodResolver
from fsd_utils import init_sentry
from fsd_utils.healthchecks.checkers import FlaskRunningChecker
from fsd_utils.healthchecks.healthcheck import Healthcheck
from fsd_utils.logging import logging
from fsd_utils.sqs_scheduler.context_aware_executor import ContextAwareExecutor
from fsd_utils.sqs_scheduler.scheduler_service import scheduler_executor

from app.notification.scheduler.notification_task_executor_service import (
    NotificationTaskExecutorService,
)
from config import Config
from openapi.utils import get_bundled_specs


def create_app() -> FlaskApp:
    init_sentry()

    connexion_app = connexion.App(
        __name__,
    )
    connexion_app.add_api(
        get_bundled_specs("/openapi/api.yml"),
        validate_responses=True,
        resolver=MethodResolver("api"),
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
    task_executor_service = NotificationTaskExecutorService(
        flask_app=flask_app,
        executor=executor,
        s3_bucket=Config.AWS_MSG_BUCKET_NAME,
        sqs_primary_url=Config.AWS_SQS_NOTIF_APP_PRIMARY_QUEUE_URL,
        task_executor_max_thread=Config.TASK_EXECUTOR_MAX_THREAD,
        sqs_batch_size=Config.SQS_BATCH_SIZE,
        visibility_time=Config.SQS_VISIBILITY_TIME,
        sqs_wait_time=Config.SQS_WAIT_TIME,
        region_name=Config.AWS_REGION,
        endpoint_url_override=Config.AWS_ENDPOINT_OVERRIDE,
        aws_access_key_id=Config.AWS_SQS_ACCESS_KEY_ID,
        aws_secret_access_key=Config.AWS_SQS_ACCESS_KEY_ID,
    )
    # Configurations for Flask-Apscheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=scheduler_executor,
        trigger="interval",
        seconds=Config.SQS_RECEIVE_MESSAGE_CYCLE_TIME,  # Run the job every 'x' seconds
        kwargs={"task_executor_service": task_executor_service},
    )
    scheduler.start()

    # Add healthchecks to flask_app
    health = Healthcheck(flask_app)
    health.add_check(FlaskRunningChecker())

    return connexion_app


app = create_app()
application = app.app
