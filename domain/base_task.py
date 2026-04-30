from abc import ABC, abstractmethod
from .interfaces import ProgressReporter

class DomainTask(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def execute(self, reporter: ProgressReporter):
        pass
