from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QPushButton
from PySide6.QtCore import Signal

class TaskView(QFrame):
    start_requested = Signal()
    cancel_requested = Signal()

    def __init__(self, title: str):
        super().__init__()
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        layout = QVBoxLayout(self)

        self.title_label = QLabel(f"<b>{title}</b>")
        layout.addWidget(self.title_label)

        self.task_id_label = QLabel("ID: -")
        layout.addWidget(self.task_id_label)

        self.status_label = QLabel("Status: PENDING")
        layout.addWidget(self.status_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)

        self.message_label = QLabel("-")
        layout.addWidget(self.message_label)

        btn_layout = QHBoxLayout()
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_requested.emit)
        btn_layout.addWidget(self.start_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setEnabled(False)
        self.cancel_button.clicked.connect(self.cancel_requested.emit)
        btn_layout.addWidget(self.cancel_button)

        layout.addLayout(btn_layout)

    def set_title(self, text: str):
        self.title_label.setText(f"<b>{text}</b>")

    def set_running(self, task_id: str):
        self.task_id_label.setText(f"ID: {task_id}")
        self.status_label.setText("Status: RUNNING")
        self.start_button.setEnabled(False)
        self.cancel_button.setEnabled(True)

    def set_final_state(self, status, message: str):
        self.status_label.setText(f"Status: {status.name}")
        self.message_label.setText(message)
        self.start_button.setEnabled(True)
        self.cancel_button.setEnabled(False)

    def set_message(self, text: str):
        self.message_label.setText(text)

    def set_progress(self, value: int):
        self.progress_bar.setValue(value)
