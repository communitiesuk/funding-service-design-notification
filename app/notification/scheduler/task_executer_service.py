import json
import threading
from concurrent.futures import as_completed
from os import getenv
from uuid import uuid4

from fsd_utils.services.aws_extended_client import SQSExtendedClient

from app.notification.model import Notification
from config import Config


class TaskExecutorService:
    def __init__(self, flask_app, executor):
        self.logger = flask_app.logger
        self.logger.info("Creating a thread pool executor to process messages in notification SQS queue")
        self.executor = executor
        self.sqs_extended_client = SQSExtendedClient(
            aws_access_key_id=Config.AWS_SQS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SQS_SECRET_ACCESS_KEY,
            region_name=Config.AWS_SQS_REGION,
            endpoint_url=getenv("AWS_ENDPOINT_OVERRIDE", None),
            large_payload_support=Config.AWS_MSG_BUCKET_NAME,
            always_through_s3=True,
            delete_payload_from_s3=True,
            logger=self.logger,
        )

    def process_messages(self):
        """
        Scheduler calling this method based on a cron job for every given second then messages will be read
        from the SQS queue in AWS and if S3 usage is allowed then it will interact each other to retrieve the messages
        """
        current_thread = threading.current_thread()
        thread_id = f"[{current_thread.name}:{current_thread.ident}]"
        self.logger.debug(f"{thread_id} Triggered schedular to get messages")

        running_threads, read_msg_ids = self._handle_message_receiving_and_processing()

        self._handle_message_delete_processing(running_threads, read_msg_ids)

        self.logger.debug(f"{thread_id} Message Processing completed and will start again later")

    def _notification_task(self, message):
        """
        Processing the message in a separate worker thread and this will call the GOV notify service to send emails
        :param message Json message
        """
        current_thread = threading.current_thread()
        thread_id = f"[{current_thread.name}:{current_thread.ident}]"
        self.logger.info(f"[{thread_id}] Notification Triggered")
        massage_id = message["sqs"]["MessageId"]
        try:
            message_body = json.loads(message["s3"])
            Notification.email_recipient(message_body)
            self.logger.info(f"{thread_id} Processed the message: {massage_id}")
            return message
        except Exception as e:
            self.logger.error(f"An error occurred while processing the message {massage_id}", e)

    def _handle_message_receiving_and_processing(self):
        """
        Handle message retrieve from the SQS service and get the json from S3 bucket
        """
        current_thread = threading.current_thread()
        thread_id = f"[{current_thread.name}:{current_thread.ident}]"
        running_threads = []
        read_msg_ids = []
        if Config.TASK_EXECUTOR_MAX_THREAD >= self.executor.queue_size():
            notification_messages = self.sqs_extended_client.receive_messages(
                Config.AWS_SQS_NOTIF_APP_PRIMARY_QUEUE_URL,
                Config.SQS_BATCH_SIZE,
                Config.SQS_VISIBILITY_TIME,
                Config.SQS_WAIT_TIME,
            )
            self.logger.debug(f"{thread_id} Message Count [{len(notification_messages)}]")
            if notification_messages:
                for message in notification_messages:
                    message_id = message["sqs"]["MessageId"]
                    self.logger.info(f"{thread_id} Message id [{message_id}]")
                    read_msg_ids.append(message["sqs"]["MessageId"])
                    task = self.executor.submit(self._notification_task, message)
                    running_threads.append(task)
        else:
            self.logger.info(f"{thread_id} Max thread limit reached hence stop reading messages from queue")

        self.logger.debug(
            f"{thread_id} Received Message count [{len(read_msg_ids)}] "
            f"Created thread count [{len(running_threads)}]"
        )
        return running_threads, read_msg_ids

    def _handle_message_delete_processing(self, running_threads, read_msg_ids):
        """
        Handling the message delete process from the SQS and S3 bucket if it is completed
        :param read_msg_ids All the message ids that taken from SQS
        :param running_threads Executing tasks to send emails
        """
        current_thread = threading.current_thread()
        thread_id = f"[{current_thread.name}:{current_thread.ident}]"
        receipt_handles_to_delete = []
        completed_msg_ids = []
        for future in as_completed(running_threads):
            try:
                msg = future.result()
                msg_id = msg["sqs"]["MessageId"]
                receipt_handles_to_delete.append(msg["sqs"])
                completed_msg_ids.append(msg_id)
                self.logger.debug(f"{thread_id} Execution completed and deleted from queue: {msg_id}")
            except Exception as e:
                self.logger.error(f"{thread_id} An error occurred while processing the message {e}")
        dif_msg_ids = [i for i in read_msg_ids if i not in completed_msg_ids]
        self.logger.debug(f"No of massages not processed [{len(dif_msg_ids)}] and msg ids are {dif_msg_ids}")
        if receipt_handles_to_delete:
            self.sqs_extended_client.delete_messages(
                Config.AWS_SQS_NOTIF_APP_PRIMARY_QUEUE_URL,
                receipt_handles_to_delete,
            )

