import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel
from domain.types import TaskType
from domain.tasks.download_factory import DownloadTaskFactory
from domain.tasks.device_monitor_factory import DeviceMonitorTaskFactory
from framework.core.registry import TaskRegistry
from framework.core.manager import TaskManager
from framework.adapters.qt.executor import QtTaskExecutor
from ui.views.task_view import TaskView
from ui.presenters.task_presenter import TaskPresenter

class MainWindow(QMainWindow):
    def __init__(self, manager: TaskManager):
        super().__init__()
        self.manager = manager
        self.setWindowTitle("Task Management System")
        self.resize(500, 600)

        central = QWidget()
        self.setCentralWidget(central)
        self.layout = QVBoxLayout(central)

        self.layout.addWidget(QLabel("URL:"))
        self.url_input = QLineEdit("https://example.com/file.zip")
        self.layout.addWidget(self.url_input)

        self.add_btn = QPushButton("Add Download Task")
        self.add_btn.clicked.connect(self.add_task)
        self.layout.addWidget(self.add_btn)

        self.tasks_container = QVBoxLayout()
        self.layout.addLayout(self.tasks_container)

    def add_task(self):
        url = self.url_input.text()
        if "monitor" in url.lower():
             view = self.manager.create_task(TaskType.DEMO, "DEVICE-X")
        else:
             view = self.manager.create_task(TaskType.DOWNLOAD, url, "/tmp/save")
        self.tasks_container.addWidget(view)

def main():
    registry = TaskRegistry()
    registry.register(TaskType.DOWNLOAD, DownloadTaskFactory)
    registry.register(TaskType.DEMO, DeviceMonitorTaskFactory)

    from framework.core.repository import JsonTaskRepository
    repo = JsonTaskRepository("tasks_persistence.json")
    executor = QtTaskExecutor()
    manager = TaskManager(executor, registry, repository=repo)
    manager.set_factories(
        view_factory=lambda title: TaskView(title),
        presenter_factory=lambda view, factory, mgr: TaskPresenter(view, factory, mgr)
    )

    app = QApplication(sys.argv)
    window = MainWindow(manager)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
