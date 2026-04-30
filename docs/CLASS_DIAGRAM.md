@startuml
interface ProgressReporter {
    +report_progress(percent: int)
    +report_message(message: str)
    +is_cancelled(): bool
}

abstract class DomainTask {
    +name: str
    +execute(reporter: ProgressReporter)
}

abstract class TaskFactory {
    +create_task(): DomainTask
    +build_title(): str
}

class TaskManager {
    -executor: TaskExecutor
    -registry: TaskRegistry
    +create_task(type, *args): TaskView
    +submit_runner(runner)
}

class QtTaskRunner {
    -domain_task: DomainTask
    -reporter: QtProgressReporter
    +run()
    +cancel()
}

ProgressReporter <|.. QtProgressReporter
ProgressReporter <|.. ConsoleProgressReporter
DomainTask <|-- DownloadTask
DomainTask <|-- DeviceMonitorTask
TaskFactory <|-- DownloadTaskFactory
TaskFactory <|-- DeviceMonitorTaskFactory

QtTaskRunner o-- DomainTask
QtTaskRunner *-- QtProgressReporter
TaskManager o-- TaskExecutor
@enduml
