@startuml
actor User
participant TaskPresenter
participant TaskManager
participant QtTaskRunner
participant DomainTask
participant QtProgressReporter
participant TaskView

User -> TaskPresenter: on_start()
TaskPresenter -> DomainTask: create via factory
TaskPresenter -> QtTaskRunner: create(task)
TaskPresenter -> TaskManager: submit_runner(runner)
TaskManager -> QtTaskRunner: start (worker thread)

activate QtTaskRunner
QtTaskRunner -> DomainTask: execute(reporter)
activate DomainTask
DomainTask -> QtProgressReporter: report_progress(val)
QtProgressReporter -> TaskView: emit signal -> update UI
DomainTask -> QtProgressReporter: is_cancelled()
DomainTask --> QtTaskRunner: return
deactivate DomainTask
QtTaskRunner -> TaskPresenter: finished signal
deactivate QtTaskRunner
@enduml
