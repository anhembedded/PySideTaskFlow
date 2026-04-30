from PySide6.QtCore import QRunnable, QThreadPool, QObject, Signal
from .executor import TaskExecutor
from ..core.interfaces import Task, TaskContext, TaskRepository
from ..core.state import TaskState
from ..core.status import TaskStatus
from ..core.events import EventManager

class QtWorkerSignals(QObject):
    updated = Signal(object)

class QtWorker(QRunnable):
    def __init__(self, task: Task, state: TaskState, context: TaskContext, repository: TaskRepository, events: EventManager):
        super().__init__()
        self.task = task
        self.state = state
        self.context = context
        self.repository = repository
        self.events = events
        self.signals = QtWorkerSignals()

    def run(self):
        self.state.status = TaskStatus.RUNNING
        self.repository.save(self.state)
        self.events.emit("task_updated", self.state)
        self.signals.updated.emit(self.state)

        try:
            result = self.task.run(self.context)
            if self.context.is_cancelled():
                self.state.status = TaskStatus.CANCELLED
            else:
                self.state.status = TaskStatus.COMPLETED
                self.state.result = result
                self.state.progress = 100
        except Exception as e:
            self.state.status = TaskStatus.FAILED
            self.state.error = str(e)
        finally:
            self.repository.save(self.state)
            self.events.emit("task_updated", self.state)
            self.signals.updated.emit(self.state)

class QtTaskExecutor(TaskExecutor):
    def __init__(self, repository: TaskRepository, events: EventManager, context_factory):
        self.repository = repository
        self.events = events
        self.context_factory = context_factory
        self.thread_pool = QThreadPool.globalInstance()
        self._cancelled_tasks = set()

    def execute(self, task: Task, task_id: str, name: str):
        state = TaskState(task_id=task_id, name=name)
        self.repository.save(state)

        context = self.context_factory(task_id, self.repository, self.events, self._cancelled_tasks)
        worker = QtWorker(task, state, context, self.repository, self.events)
        self.thread_pool.start(worker)

    def cancel(self, task_id: str):
        self._cancelled_tasks.add(task_id)
