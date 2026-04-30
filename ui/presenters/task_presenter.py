from PySide6.QtCore import QObject, Slot
from domain.factory import TaskFactory
from domain.types import TaskStatus
from framework.adapters.qt.runner import QtTaskRunner

class TaskPresenter(QObject):
    def __init__(self, view, factory: TaskFactory, manager):
        super().__init__(view) # Parent is view to avoid GC
        self.view = view
        self.factory = factory
        self.manager = manager
        self.runner = None

        self.view.start_requested.connect(self.on_start)
        self.view.cancel_requested.connect(self.on_cancel)

    @Slot()
    def on_start(self):
        task = self.factory.create_task()
        # manager should have repository
        repo = getattr(self.manager, '_repository', None)
        self.runner = QtTaskRunner(task, repository=repo)

        self.runner.signals.progress.connect(self.view.set_progress)
        self.runner.signals.message.connect(self.view.set_message)
        self.runner.signals.error.connect(self.on_runner_error)
        self.runner.signals.finished.connect(self.on_runner_finished)

        self.view.set_running(self.runner.task_id)
        self.manager.submit_runner(self.runner)

    @Slot()
    def on_cancel(self):
        if self.runner:
            self.runner.cancel()

    @Slot(str)
    def on_runner_error(self, msg: str):
        self.view.set_message(f"Error: {msg}")

    @Slot(object)
    def on_runner_finished(self, status: TaskStatus):
        self.view.set_final_state(status, f"Finished with {status.name}")
        self.runner = None

    def reconfigure(self, factory: TaskFactory):
        self.factory = factory
        self.view.set_title(self.factory.build_title())
        # Reset UI
        self.view.set_progress(0)
        self.view.set_message("Reconfigured")
