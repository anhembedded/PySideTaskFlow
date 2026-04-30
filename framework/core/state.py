from dataclasses import dataclass, field
from typing import Any, Optional, Dict
from domain.types import TaskStatus

@dataclass
class TaskState:
    task_id: str
    name: str
    status: TaskStatus = TaskStatus.PENDING
    progress: int = 0
    result: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
