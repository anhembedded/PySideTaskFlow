import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from PySide6.QtWidgets import QApplication, QMainWindow
from framework.core.repository import JsonTaskRepository
from framework.core.events import EventManager
from framework.runtime.qt_runtime import QtTaskExecutor
from framework.adapters.qt.progress_adapter import QtProgressAdapter
from ui.views.task_list_view import TaskListView
from ui.presenters.task_presenter import TaskPresenter
from domain.tasks import register_domain_tasks

class DashboardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Dashboard")
        self.resize(600, 400)

        register_domain_tasks()

        self.repo = JsonTaskRepository("dashboard_tasks.json")
        self.events = EventManager()

        def context_factory(task_id, repository, events, cancelled_set):
            return QtProgressAdapter(task_id, repository, events, cancelled_set)

        self.executor = QtTaskExecutor(self.repo, self.events, context_factory)

        self.view = TaskListView()
        self.setCentralWidget(self.view)

        self.presenter = TaskPresenter(self.view, self.executor, self.repo, self.events)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardApp()
    window.show()
    sys.exit(app.exec())
