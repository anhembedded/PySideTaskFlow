from abc import ABC, abstractmethod
from ..core.interfaces import Task

class TaskExecutor(ABC):
    @abstractmethod
    def execute(self, task: Task, task_id: str, name: str):
        pass

    @abstractmethod
    def cancel(self, task_id: str):
        pass
