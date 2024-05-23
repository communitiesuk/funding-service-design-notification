from concurrent.futures import ThreadPoolExecutor
from contextvars import copy_context


class ContextAwareExecutor:

    def __init__(self, max_workers, thread_name_prefix, flask_app):
        self.executor = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix=thread_name_prefix)
        self.flask_app = flask_app

    def queue_size(self):
        return self.executor._work_queue.qsize()

    def submit(self, fn, *args, **kwargs):
        ctx = copy_context()
        future = self.executor.submit(ctx.run, self.wrap_function(fn), *args, **kwargs)
        return future

    def wrap_function(self, fn):
        def wrapped(*args, **kwargs):
            with self.flask_app.app_context():
                return fn(*args, **kwargs)

        return wrapped
