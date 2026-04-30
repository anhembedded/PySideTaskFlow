from PySide6.QtCore import QObject, Signal
from domain.types import TaskStatus

class TaskSignals(QObject):
    progress = Signal(int)
    message = Signal(str)
    error = Signal(str)
    finished = Signal(object) # TaskStatus
