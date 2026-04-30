from abc import ABC, abstractmethod
from .state import TaskState

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
