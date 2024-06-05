import time
import unittest
from unittest.mock import MagicMock
from unittest.mock import patch
from uuid import uuid4

import boto3
import pytest
from fsd_utils.sqs_scheduler.context_aware_executor import ContextAwareExecutor
from moto import mock_aws

from app.notification.scheduler.notification_task_executor_service import (
    NotificationTaskExecutorService,
)
from config import Config
from tests.test_task_executor_service.test_data_util import send_message_to_queue


class TestNotificationTaskExecutorService(unittest.TestCase):

    @mock_aws
    @pytest.mark.usefixtures("live_server")
    def test_message_in_mock_environment_processing_without_errors(self):
        """
        This test ensure that when message is there and if no errors occurred while processing the message
        then successfully removed it from the queue
        """
        self._mock_aws_client()
        self._add_data_to_queue()

        with patch(
            "app.notification.model.notifier.Notifier.send_submitted_application"
        ) as mocked_send_submitted_application:
            mocked_send_submitted_application.return_value = "", 200
            self.task_executor.process_messages()

        self._check_is_data_available(0)

    @mock_aws
    @pytest.mark.usefixtures("live_server")
    def test_message_in_mock_environment_processing_with_errors(self):
        """
        This test ensure that when message is there and if errors occurred while processing the message
        then the message remain as is in the queue
        (AWS will automatically put the message into the DLQ for reprocessing)
        """
        self._mock_aws_client()
        self._add_data_to_queue()

        with patch(
            "app.notification.model.notifier.Notifier.send_submitted_application"
        ) as mocked_send_submitted_application:
            mocked_send_submitted_application.side_effect = Exception("Error calling notification service")
            self.task_executor.process_messages()
        time.sleep(5)
        self._check_is_data_available(1)

    def _mock_aws_client(self):
        """
        Mocking aws resources and this will act as real aws environment behaviour
        """
        self.flask_app = MagicMock()
        self.executor = ContextAwareExecutor(max_workers=10, thread_name_prefix="NotifTask", flask_app=self.flask_app)
        s3_connection = boto3.client(
            "s3", region_name="us-east-1", aws_access_key_id="test_accesstoken", aws_secret_access_key="secret_key"
        )
        sqs_connection = boto3.client(
            "sqs", region_name="us-east-1", aws_access_key_id="test_accesstoken", aws_secret_access_key="secret_key"
        )
        s3_connection.create_bucket(Bucket=Config.AWS_MSG_BUCKET_NAME)
        self.queue_response = sqs_connection.create_queue(
            QueueName="notif-queue.fifo", Attributes={"FifoQueue": "true"}
        )
        Config.AWS_SQS_NOTIF_APP_PRIMARY_QUEUE_URL = self.queue_response["QueueUrl"]
        self.task_executor = NotificationTaskExecutorService(
            flask_app=MagicMock(),
            executor=self.executor,
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
        self.task_executor.sqs_extended_client.sqs_client = sqs_connection
        self.task_executor.sqs_extended_client.s3_client = s3_connection

    def _add_data_to_queue(self):
        """
        Adding test data into the queue
        """
        for x in range(1):
            message_id = self.task_executor.sqs_extended_client.submit_single_message(
                queue_url=self.queue_response["QueueUrl"],
                message=send_message_to_queue,
                message_group_id="import_applications_group",
                message_deduplication_id=str(uuid4()),  # ensures message uniqueness
            )
            assert message_id is not None

    def _check_is_data_available(self, count):
        response = self.task_executor.sqs_extended_client.receive_messages(
            queue_url=self.queue_response["QueueUrl"], max_number=1
        )
        assert len(response) == count
