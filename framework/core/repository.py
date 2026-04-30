import json
import os
import threading
from .interfaces import TaskRepository
from .state import TaskState
from .status import TaskStatus

class JsonTaskRepository(TaskRepository):
    def __init__(self, filepath: str):
        self.filepath = filepath
        self._lock = threading.Lock()
        self._ensure_file()

    def _ensure_file(self):
        with self._lock:
            if not os.path.exists(self.filepath):
                with open(self.filepath, 'w') as f:
                    json.dump({}, f)

    def save(self, state: TaskState):
        with self._lock:
            data = self._read_all_unlocked()
            data[state.task_id] = {
                "task_id": state.task_id,
                "name": state.name,
                "status": state.status.name,
                "progress": state.progress,
                "result": str(state.result) if state.result is not None else None,
                "error": state.error,
                "metadata": state.metadata
            }
            with open(self.filepath, 'w') as f:
                json.dump(data, f, indent=4)

    def get(self, task_id: str) -> TaskState:
        with self._lock:
            data = self._read_all_unlocked()
            if task_id in data:
                return self._to_state(data[task_id])
            return None

    def get_all(self) -> list[TaskState]:
        with self._lock:
            data = self._read_all_unlocked()
            return [self._to_state(v) for v in data.values()]

    def _read_all_unlocked(self) -> dict:
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _to_state(self, d: dict) -> TaskState:
        return TaskState(
            task_id=d["task_id"],
            name=d["name"],
            status=TaskStatus[d["status"]],
            progress=d["progress"],
            result=d.get("result"),
            error=d.get("error"),
            metadata=d.get("metadata", {})
        )
