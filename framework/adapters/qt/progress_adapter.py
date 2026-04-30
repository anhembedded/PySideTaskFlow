from ...core.interfaces import TaskContext, TaskRepository
from ...core.events import EventManager

class QtProgressAdapter(TaskContext):
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

    def is_cancelled(self) -> bool:
        return self.task_id in self.cancelled_set

    def log(self, message: str):
        state = self.repository.get(self.task_id)
        if state:
            # We could store logs in state metadata if needed
            if "logs" not in state.metadata:
                state.metadata["logs"] = []
            state.metadata["logs"].append(message)
            self.repository.save(state)
        self.events.emit("task_log", {"task_id": self.task_id, "message": message})
