# Task Framework Architecture

The framework follows Clean Architecture principles, ensuring strict separation of concerns.

## Layers

1.  **Core Layer**: Pure Python logic. Contains Task interfaces, State, Status, Repository interfaces, and the Event System. No external dependencies (like Qt).
2.  **Runtime Layer**: Manages execution. Provides implementations for both PySide6 (QThreadPool) and CLI (threading).
3.  **Adapter Layer**: Bridges the Core with specific runtimes/UIs. Maps `TaskContext` actions to signals or console output.
4.  **Domain Layer**: Contains the actual business logic (Tasks).
5.  **UI/CLI Layer**: User-facing components.

## Data Flow

Task (Domain) -> TaskExecutor (Runtime) -> TaskContext (Adapter) -> TaskRepository (Core) -> Presenter (UI) -> View (UI)
