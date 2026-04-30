from PySide6.QtCore import QThreadPool
from framework.core.executor import TaskExecutor
from domain.base_task import DomainTask
from domain.interfaces import ProgressReporter
from domain.types import TaskStatus
from .runner import QtTaskRunner

class QtTaskExecutor(TaskExecutor):
    def __init__(self):
        self.pool = QThreadPool.globalInstance()

    def execute(self, task: DomainTask, reporter: ProgressReporter) -> TaskStatus:
        # This standard execute might be used for synchronous calls or
        # different runner types. But TaskManager uses execute_runner.
        raise NotImplementedError("Use execute_runner for QtTaskRunner")

    def execute_runner(self, runner: QtTaskRunner):
        self.pool.start(runner)
