from app.notification.scheduler.task_executer_service import TaskExecutorService


def scheduler_executor(task_executor_service: TaskExecutorService):
    task_executor_service.process_messages()
