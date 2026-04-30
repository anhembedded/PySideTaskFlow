import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton
from framework.core.repository import JsonTaskRepository
from framework.core.events import EventManager
from framework.runtime.qt_runtime import QtTaskExecutor
from framework.adapters.qt.progress_adapter import QtProgressAdapter
from framework.adapters.qt.event_bridge import QtEventBridge
from domain.tasks import register_domain_tasks, DeviceMonitorTask
import uuid

class DeviceMonitorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Device Monitor")
        self.resize(400, 300)

        register_domain_tasks()
        self.repo = JsonTaskRepository("device_tasks.json")
        self.events = EventManager()
        self.bridge = QtEventBridge(self.events)

        def context_factory(task_id, repository, events, cancelled_set):
            return QtProgressAdapter(task_id, repository, events, cancelled_set)

        self.executor = QtTaskExecutor(self.repo, self.events, context_factory)

        central = QWidget()
        layout = QVBoxLayout(central)
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        layout.addWidget(self.log_view)

        self.start_btn = QPushButton("Start Monitoring")
        self.start_btn.clicked.connect(self.start_monitor)
        layout.addWidget(self.start_btn)

        self.setCentralWidget(central)

        self.bridge.task_log.connect(self.on_log)

    def start_monitor(self):
        task_id = str(uuid.uuid4())[:8]
        self.executor.execute(DeviceMonitorTask(), task_id, "DeviceMonitor")
        self.start_btn.setEnabled(False)

    def on_log(self, data):
        self.log_view.append(data["message"])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DeviceMonitorApp()
    window.show()
    sys.exit(app.exec())
