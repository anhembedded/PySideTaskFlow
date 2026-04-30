from framework.core.events import EventManager
from framework.runtime.executor import TaskExecutor
from framework.core.registry import TaskRegistry
import uuid

from framework.adapters.qt.event_bridge import QtEventBridge

class TaskPresenter:
    def __init__(self, view, executor: TaskExecutor, repository, events: EventManager):
        self.view = view
        self.executor = executor
        self.repository = repository
        self.events = events

        self.bridge = QtEventBridge(self.events)

        self.view.start_task_clicked.connect(self.on_start_task)
        self.bridge.task_updated.connect(self.refresh_view)

    def on_start_task(self, task_name: str):
        task_cls = TaskRegistry.get_task_class(task_name)
        if task_cls:
            task_id = str(uuid.uuid4())[:8]
            self.executor.execute(task_cls(), task_id, task_name)

    def refresh_view(self, _=None):
        tasks = self.repository.get_all()
        # In a real app, you'd ensure this runs on the UI thread.
        # Since we use Qt signals in QtTaskExecutor/QtProgressAdapter, it should be safe if handled via signals.
        self.view.update_tasks(tasks)
