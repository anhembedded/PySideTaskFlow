from abc import ABC, abstractmethod

class ProgressReporter(ABC):
    @abstractmethod
    def report_progress(self, percent: int):
        pass

    @abstractmethod
    def report_message(self, message: str):
        pass

    @abstractmethod
    def is_cancelled(self) -> bool:
        pass
