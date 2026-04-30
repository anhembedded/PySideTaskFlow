from PySide6.QtCore import QRunnable, Signal, QObject
from domain.base_task import DomainTask
from domain.types import TaskStatus
from .signals import TaskSignals
from .reporter import QtProgressReporter
import uuid

from framework.core.state import TaskState

class QtTaskRunner(QRunnable):
    def __init__(self, domain_task: DomainTask, repository=None):
        super().__init__()
        self.domain_task = domain_task
        self.repository = repository
        self.signals = TaskSignals()
        self.reporter = QtProgressReporter(self.signals)
        self.task_id = str(uuid.uuid4())[:8]
        self.status = TaskStatus.PENDING
        self._state = TaskState(task_id=self.task_id, name=self.domain_task.name)
        if self.repository:
            self.repository.save(self._state)

    def run(self):
        self.status = TaskStatus.RUNNING
        self._state.status = self.status
        if self.repository:
            self.repository.save(self._state)

        # Connect signals to update state if repository exists
        if self.repository:
            self.signals.progress.connect(self._update_progress)
            self.signals.message.connect(self._update_message)

        try:
            self.domain_task.execute(self.reporter)
            if self.reporter.is_cancelled():
                self.status = TaskStatus.CANCELLED
            else:
                self.status = TaskStatus.COMPLETED
        except Exception as e:
            self.status = TaskStatus.FAILED
            self._state.error = str(e)
            self.signals.error.emit(str(e))
        finally:
            self._state.status = self.status
            if self.repository:
                self.repository.save(self._state)
            self.signals.finished.emit(self.status)

    def _update_progress(self, val):
        self._state.progress = val
        if self.repository: self.repository.save(self._state)

    def _update_message(self, msg):
        self._state.metadata["last_message"] = msg
        if self.repository: self.repository.save(self._state)

    def cancel(self):
        self.reporter.cancel()
