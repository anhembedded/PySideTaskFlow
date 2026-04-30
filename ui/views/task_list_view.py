from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QProgressBar
from PySide6.QtCore import Signal, Slot

class TaskListView(QWidget):
    start_task_clicked = Signal(str)
    cancel_task_clicked = Signal(str)

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.status_label = QLabel("Task Dashboard")
        self.layout.addWidget(self.status_label)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Status", "Progress"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table)

        self.btn_layout = QVBoxLayout()
        self.start_demo_btn = QPushButton("Start DemoTask")
        self.start_demo_btn.clicked.connect(lambda: self.start_task_clicked.emit("DemoTask"))
        self.btn_layout.addWidget(self.start_demo_btn)

        self.start_long_btn = QPushButton("Start LongRunningTask")
        self.start_long_btn.clicked.connect(lambda: self.start_task_clicked.emit("LongRunningTask"))
        self.btn_layout.addWidget(self.start_long_btn)

        self.layout.addLayout(self.btn_layout)

    def update_tasks(self, tasks):
        self.table.setRowCount(len(tasks))
        for i, task in enumerate(tasks):
            self.table.setItem(i, 0, QTableWidgetItem(task.task_id))
            self.table.setItem(i, 1, QTableWidgetItem(task.name))
            self.table.setItem(i, 2, QTableWidgetItem(task.status.name))

            progress_bar = QProgressBar()
            progress_bar.setValue(task.progress)
            self.table.setCellWidget(i, 3, progress_bar)
