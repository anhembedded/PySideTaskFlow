from abc import ABC, abstractmethod
from domain.base_task import DomainTask
from domain.interfaces import ProgressReporter
from domain.types import TaskStatus

class TaskExecutor(ABC):
    @abstractmethod
    def execute(self, task: DomainTask, reporter: ProgressReporter) -> TaskStatus:
        pass
