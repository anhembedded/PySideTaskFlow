from typing import Dict, Type
from domain.types import TaskType
from domain.factory import TaskFactory

class TaskRegistry:
    def __init__(self):
        self._mapping: Dict[TaskType, Type[TaskFactory]] = {}

    def register(self, task_type: TaskType, factory_cls: Type[TaskFactory]):
        self._mapping[task_type] = factory_cls

    def get_factory(self, task_type: TaskType, *args, **kwargs) -> TaskFactory:
        factory_cls = self._mapping.get(task_type)
        if factory_cls:
            return factory_cls(*args, **kwargs)
        raise ValueError(f"No factory registered for {task_type}")
