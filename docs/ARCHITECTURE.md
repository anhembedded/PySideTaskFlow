# Scalable Task Framework

## Overview
This framework provides a decoupled architecture for running background tasks in both PySide6 GUI and CLI environments.

## Architecture
- **Domain Layer**: Contains business logic (Tasks) and factories. Independent of Qt.
- **Application Core**: Manages task registration, life cycle, and persistence.
- **Adapters**: Bridges the core with specific runtimes (Qt with QThreadPool, Console with direct execution).
- **UI Layer**: MVP pattern using PySide6.

## Key Components
- `TaskRegistry`: Maps `TaskType` to `TaskFactory`.
- `TaskManager`: Orchestrates task creation and execution.
- `TaskRepository`: Persists task state to JSON.
- `QtTaskRunner`: Executes domain tasks in background threads safely.

## Usage
Run `python3 main.py` to choose between GUI and CLI modes.
