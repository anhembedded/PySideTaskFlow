@startuml
interface Task {
    +run(ctx: TaskContext): Any
}

interface TaskContext {
    +report_progress(value: int)
    +is_cancelled(): bool
    +log(message: str)
}

class TaskState {
    +task_id: str
    +status: TaskStatus
    +progress: int
    +result: Any
    +error: str
}

interface TaskRepository {
    +save(state: TaskState)
    +get(id: str): TaskState
    +get_all(): List[TaskState]
}

abstract class TaskExecutor {
    +execute(task: Task, id: str, name: str)
    +cancel(id: str)
}

class QtTaskExecutor extends TaskExecutor
class CLITaskExecutor extends TaskExecutor

class QtProgressAdapter implements TaskContext
class CLIProgressAdapter implements TaskContext

Task .right.> TaskContext
TaskExecutor --> Task
TaskExecutor --> TaskRepository
@enduml
