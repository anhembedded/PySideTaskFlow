from typing import Dict, Type
from .interfaces import Task

class TaskRegistry:
    _tasks: Dict[str, Type[Task]] = {}

    @classmethod
    def register(cls, name: str, task_cls: Type[Task]):
        cls._tasks[name] = task_cls

    @classmethod
    def get_task_class(cls, name: str) -> Type[Task]:
        return cls._tasks.get(name)

    @classmethod
    def list_tasks(cls) -> list[str]:
        return list(cls._tasks.keys())
