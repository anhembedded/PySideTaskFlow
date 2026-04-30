from abc import ABC, abstractmethod
from typing import Any
from .state import TaskState

class TaskContext(ABC):
    @abstractmethod
    def report_progress(self, value: int):
        pass

    @abstractmethod
    def is_cancelled(self) -> bool:
        pass

    @abstractmethod
    def log(self, message: str):
        pass

class Task(ABC):
    @abstractmethod
    def run(self, ctx: TaskContext) -> Any:
        pass

class TaskRepository(ABC):
    @abstractmethod
    def save(self, state: TaskState):
        pass

    @abstractmethod
    def get(self, task_id: str) -> TaskState:
        pass

    @abstractmethod
    def get_all(self) -> list[TaskState]:
        pass
