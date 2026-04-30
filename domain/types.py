from enum import Enum, auto

class TaskStatus(Enum):
    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    CANCELLED = auto()
    FAILED = auto()

class TaskType(Enum):
    DOWNLOAD = auto()
    DEMO = auto()
