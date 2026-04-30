You are a senior software architect specializing in Python, PySide6 (Qt), and clean architecture.

I want you to design and implement a **production-quality, scalable task-based UI framework** with support for BOTH GUI (PySide6) and CLI (headless mode).

The system must follow clean architecture principles with strict separation between Core, Domain, Adapters, and UI.

---

# 🎯 GOAL

Build a reusable framework that:

* Runs background tasks using a thread pool
* Supports progress, result, error reporting
* Works in BOTH:

  * GUI mode (PySide6)
  * CLI mode (no GUI)
* Keeps Domain completely independent from UI and Qt

---

# 🧱 ARCHITECTURE (MANDATORY)

## 1. Core Layer (PURE, NO QT DEPENDENCY)

Location: framework/core/

Must contain:

* Task (abstract base class)
* TaskContext (VERY IMPORTANT)
* TaskState (data class)
* TaskStatus (enum)
* TaskRepository (store for task states)
* Event system (simple pub/sub or observer abstraction)

### Task requirements:

```python
def run(self, ctx: TaskContext):
    ...
```

### TaskContext must provide:

* report_progress(value: int)
* is_cancelled()
* log(message: str)

NO Qt imports allowed in core.

---

## 2. Runtime Layer

Location: framework/runtime/

* TaskExecutor (manages execution)
* Worker abstraction

Provide:

### Qt Runtime:

* Uses QThreadPool + QRunnable
* Emits signals safely

### CLI Runtime:

* Runs tasks synchronously or via threading
* Prints output to console

---

## 3. Adapter Layer

Location: framework/adapters/

Split into:

* qt/
* cli/

Adapters bridge:

Core ↔ Runtime ↔ UI

Examples:

* QtProgressAdapter (maps TaskContext → Qt signals)
* CLIProgressAdapter (maps TaskContext → print/log)

Adapters must isolate framework from UI/CLI specifics.

---

## 4. Domain Layer

Location: domain/

* Contains only task implementations
* MUST NOT import Qt
* MUST NOT depend on UI

Example:

* DemoTask
* LongRunningTask

---

## 5. UI Layer (PySide6)

Location: ui/

Use MVP pattern:

* View (Qt widgets only)
* Presenter (business logic)

UI must:

* Display list of tasks
* Show:

  * task_id
  * status
  * progress
* Have "Start Task" button

UI must NOT:

* access threads directly
* hold Worker references

---

## 6. CLI Layer

Location: cli/

* Provide a runner script
* Run tasks from command line
* Print progress and results

---

# 🔄 DATA FLOW (STRICT)

Task (Domain)
↓
TaskExecutor
↓
TaskContext / Adapter
↓
TaskRepository (state updated)
↓
Presenter / CLI
↓
View or Console

---

# 📦 TASK SYSTEM REQUIREMENTS

Each task must have:

* unique task_id
* TaskState tracked in repository

TaskState must include:

* id
* status (pending, running, completed, failed, cancelled)
* progress (0–100)
* result
* error

---

# ⚙️ THREADING

* GUI mode: QThreadPool + QRunnable
* CLI mode: standard Python execution or threading
* No UI updates from worker threads

---

# 📊 UML & DOCUMENTATION (MANDATORY)

Generate:

1. High-level architecture diagram
2. Class diagram
3. Sequence diagram (task execution flow)

Use PlantUML or clear text diagrams.

---

# 🧪 SAMPLE APPLICATIONS (MANDATORY)

Create at least 3 sample apps:

1. Task Dashboard (GUI)

   * list tasks
   * show progress
   * allow multiple concurrent tasks

2. Device Monitor (GUI, simulation ok)

   * simulate periodic data updates

3. Batch Runner (CLI)

   * run multiple tasks
   * print logs

---

# 📁 PROJECT STRUCTURE

framework/
core/
runtime/
adapters/
qt/
cli/

domain/
tasks/

ui/
views/
presenters/

cli/
runner.py

apps/
task_dashboard/
device_monitor/
batch_runner/

main.py

---

# 🧩 DESIGN PRINCIPLES (VERY IMPORTANT)

* Loose coupling between UI and Domain
* No Qt in Domain
* Core must be framework-agnostic
* Use:

  * MVP pattern
  * Observer pattern
  * Command pattern (Task)
* Clean, readable, maintainable code

---

# 🚫 DO NOT

* Do NOT mix UI and domain logic
* Do NOT directly update UI from threads
* Do NOT tightly couple adapters
* Do NOT skip TaskContext

---

# 🎁 OUTPUT

* Full working code
* File-by-file structure
* Clear comments explaining architecture
* Runnable examples for both GUI and CLI

---

# 🎯 FINAL RESULT

A mini **cross-mode task execution framework**:

* GUI app (PySide6)
* CLI tool
* Shared core logic

Focus on correctness, architecture, and extensibility.
