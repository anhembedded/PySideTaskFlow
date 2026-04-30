from ...core.interfaces import TaskContext, TaskRepository
from ...core.events import EventManager

class CLIProgressAdapter(TaskContext):
    def __init__(self, task_id: str, repository: TaskRepository, events: EventManager, cancelled_set: set):
        self.task_id = task_id
        self.repository = repository
        self.events = events
        self.cancelled_set = cancelled_set

    def report_progress(self, value: int):
        state = self.repository.get(self.task_id)
        if state:
            state.progress = value
            self.repository.save(state)
            self.events.emit("task_updated", state)
            print(f"[Task {self.task_id}] Progress: {value}%")

    def is_cancelled(self) -> bool:
        return self.task_id in self.cancelled_set

    def log(self, message: str):
        print(f"[Task {self.task_id}] LOG: {message}")
