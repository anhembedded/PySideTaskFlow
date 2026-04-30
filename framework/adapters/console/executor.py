from framework.core.executor import TaskExecutor
from domain.base_task import DomainTask
from domain.interfaces import ProgressReporter
from domain.types import TaskStatus

class ConsoleTaskExecutor(TaskExecutor):
    def execute(self, task: DomainTask, reporter: ProgressReporter) -> TaskStatus:
        try:
            task.execute(reporter)
            return TaskStatus.COMPLETED
        except Exception as e:
            print(f"Error: {e}")
            return TaskStatus.FAILED
