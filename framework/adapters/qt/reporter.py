from PySide6.QtCore import QMutex, QMutexLocker
from domain.interfaces import ProgressReporter
from .signals import TaskSignals

class QtProgressReporter(ProgressReporter):
    def __init__(self, signals: TaskSignals):
        self._signals = signals
        self._cancelled = False
        self._mutex = QMutex()

    def report_progress(self, percent: int):
        self._signals.progress.emit(percent)

    def report_message(self, message: str):
        self._signals.message.emit(message)

    def is_cancelled(self) -> bool:
        with QMutexLocker(self._mutex):
            return self._cancelled

    def cancel(self):
        with QMutexLocker(self._mutex):
            self._cancelled = True
