from PySide6.QtCore import QObject, Signal
from framework.core.events import EventManager

class QtEventBridge(QObject):
    task_updated = Signal(object)
    task_log = Signal(object)

    def __init__(self, event_manager: EventManager):
        super().__init__()
        self.event_manager = event_manager
        self.event_manager.subscribe("task_updated", self._on_task_updated)
        self.event_manager.subscribe("task_log", self._on_task_log)

    def _on_task_updated(self, state):
        self.task_updated.emit(state)

    def _on_task_log(self, data):
        self.task_log.emit(data)
