import json
import threading

from fsd_utils.sqs_scheduler.task_executer_service import TaskExecutorService

from app.notification.model import Notification


class NotificationTaskExecutorService(TaskExecutorService):
    def message_executor(self, message):
        """
        Processing the message in a separate worker thread and this will call the GOV notify service to send emails
        :param message Json message
        """
        current_thread = threading.current_thread()
        thread_id = f"[{current_thread.name}:{current_thread.ident}]"
        self.logger.info(f"[{thread_id}] Notification Triggered")
        message_id = message["sqs"]["MessageId"]
        try:
            message_body = json.loads(message["s3"])
            Notification.email_recipient(message_body)
            self.logger.info(f"{thread_id} Processed the message: {message_id}")
            return message
        except Exception as e:
            self.logger.error(f"An error occurred while processing the message {message_id}", e)
