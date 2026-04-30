@startuml
actor User
participant Presenter
participant TaskExecutor
participant Task
participant TaskContext
participant TaskRepository
participant EventManager

User -> Presenter: Click "Start Task"
Presenter -> TaskExecutor: execute(task, id, name)
TaskExecutor -> TaskRepository: save(PENDING state)
TaskExecutor -> TaskExecutor: start Worker thread
activate TaskExecutor

TaskExecutor -> Task: run(ctx)
activate Task
Task -> TaskContext: report_progress(50)
TaskContext -> TaskRepository: save(progress=50)
TaskContext -> EventManager: emit("task_updated")
EventManager -> Presenter: refresh_view()

Task --> TaskExecutor: return result
deactivate Task

TaskExecutor -> TaskRepository: save(COMPLETED state)
TaskExecutor -> EventManager: emit("task_updated")
deactivate TaskExecutor
@enduml
