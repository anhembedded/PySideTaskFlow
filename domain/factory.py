from abc import ABC, abstractmethod
from .base_task import DomainTask

class TaskFactory(ABC):
    @abstractmethod
    def create_task(self) -> DomainTask:
        pass

    @abstractmethod
    def build_title(self) -> str:
        pass
