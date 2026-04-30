# Software Design Document (SDD)

## Project: Task-Oriented UI Framework (PySide6 + CLI)

---

# 1. Overview

## 1.1 Purpose

Framework này cung cấp một nền tảng để xây dựng ứng dụng desktop (PySide6) và CLI dựa trên **task execution model**, với mục tiêu:

* Tách biệt hoàn toàn Domain logic khỏi UI
* Hỗ trợ đa luồng an toàn (GUI không bị block)
* Cho phép reuse domain cho cả GUI và CLI
* Dễ test, dễ mở rộng

---

## 1.2 Design Goals

* Loose coupling giữa:

  * Domain
  * UI
  * Runtime (threading)
* Không phụ thuộc Qt trong Domain
* Hỗ trợ Dependency Injection
* Không “magic binding” quá mức
* API rõ ràng, predictable

---

## 1.3 Non-Goals

* Không build full DI container
* Không ép buộc UI pattern (MVP/MVVM)
* Không quản lý lifecycle của QWidget

---

# 2. High-Level Architecture

```
+----------------------+
|      UI Layer        |
|  (View + Presenter)  |
+----------+-----------+
           |
           v
+----------------------+
|   Application Layer  |
| (composition root)   |
+----------+-----------+
           |
           v
+----------------------+
|    Framework Core    |
|  Task + Runtime API  |
+----------+-----------+
           |
           v
+----------------------+
|     Adapters         |
|  Qt / CLI Runtime    |
+----------+-----------+
           |
           v
+----------------------+
|      Domain          |
|    Task logic        |
+----------------------+
```

---

# 3. Core Concepts

## 3.1 Task

```python
class Task(ABC):
    def run(self, ctx: TaskContext) -> Any:
        pass
```

* Domain logic entry point
* Không phụ thuộc UI hoặc Qt

---

## 3.2 TaskContext

```python
class TaskContext:
    def report_progress(self, value: int): ...
    def report_message(self, message: str): ...
    def log(self, message: str): ...
    def is_cancelled(self) -> bool: ...
```

**Mục đích:**

* Abstraction duy nhất để task giao tiếp với runtime
* Tránh leak adapter (Qt / CLI)

---

## 3.3 TaskState

```python
@dataclass
class TaskState:
    id: str
    status: TaskStatus
    progress: int
    result: Any
    error: Optional[str]
```

---

## 3.4 TaskStatus

```python
class TaskStatus(Enum):
    PENDING
    RUNNING
    COMPLETED
    FAILED
    CANCELLED
```

---

## 3.5 TaskHandle

```python
class TaskHandle:
    def cancel(self): ...
    def subscribe(self, callback): ...
    def get_state(self) -> TaskState: ...
```

**Mục đích:**

* Interface thống nhất cho cả Qt và CLI
* Tránh mismatch async/sync

---

# 4. Framework Core

## 4.1 TaskExecutor

```python
class TaskExecutor(ABC):
    def submit(self, task: Task) -> TaskHandle:
        pass
```

* Entry point để chạy task
* Không expose threading details

---

## 4.2 TaskRepository

```python
class TaskRepository:
    def add(self, state: TaskState): ...
    def update(self, state: TaskState): ...
    def get(self, task_id: str) -> TaskState: ...
```

* Source of truth cho task state
* Có thể emit event khi state thay đổi

---

## 4.3 TaskRegistry

```python
class TaskRegistry:
    def register(self, task_type, factory): ...
    def create(self, task_type, *args, **kwargs) -> Task: ...
```

---

## 4.4 TaskFactory

```python
class TaskFactory(ABC):
    def create(self) -> Task:
        pass
```

---

# 5. Runtime Layer

## 5.1 Qt Implementation

* QThreadPool
* QRunnable

### QtTaskExecutor

```python
class QtTaskExecutor(TaskExecutor):
    def submit(self, task: Task) -> TaskHandle:
        ...
```

### Responsibilities

* Tạo Worker
* Bind TaskContext → Qt signals
* Dispatch vào thread pool

---

## 5.2 CLI Implementation

```python
class CLITaskExecutor(TaskExecutor):
    def submit(self, task: Task) -> TaskHandle:
        ...
```

* Chạy synchronous hoặc threading
* Output ra console

---

# 6. Adapter Layer

## 6.1 Nguyên tắc

* Adapter convert:

  * TaskContext → Qt Signal
  * TaskContext → CLI output
* Không leak Qt vào core

---

# 7. UI Integration

## 7.1 Nguyên tắc

* Framework KHÔNG quản lý View lifecycle
* Framework KHÔNG giữ reference Presenter

---

## 7.2 Presenter

```python
class BasePresenter:
    def __init__(self, executor: TaskExecutor):
        self.executor = executor

    def bind(self, view):
        pass
```

---

## 7.3 PresenterFactory

```python
class PresenterFactory:
    def register(self, view_cls, presenter_cls): ...

    def create(self, view):
        ...
```

---

## 7.4 Helper API (optional)

```python
def create_view(view_cls):
    view = view_cls()
    presenter = factory.create(view)
    presenter.bind(view)
    return view
```

👉 Chỉ là helper, không phải core logic

---

# 8. Data Flow

```
User Action
    ↓
Presenter
    ↓
TaskExecutor.submit()
    ↓
Worker Thread
    ↓
Task.run(ctx)
    ↓
TaskContext → Adapter
    ↓
TaskRepository update
    ↓
Presenter notified
    ↓
View update
```

---

# 9. Threading Model

* GUI:

  * QThreadPool + QRunnable
  * Signal-slot queued connection

* CLI:

  * synchronous / threading

---

# 10. Dependency Injection

* Composition root nằm ở application
* Framework không tạo singleton
* Dependency được inject:

```python
executor = QtTaskExecutor()
repo = TaskRepository()
presenter = MyPresenter(executor)
```

---

# 11. Error Handling

* Task exception → catch tại Worker
* Update TaskState.error
* Emit event / notify subscriber

---

# 12. Cancellation

* TaskContext giữ flag cancelled
* Task tự check:

```python
if ctx.is_cancelled():
    return
```

---

# 13. Testing Strategy

* Mock TaskExecutor trong Presenter test
* Test Task độc lập (không cần Qt)
* Test CLI runtime riêng

---

# 14. Project Structure

```
framework/
    core/
        task.py
        task_context.py
        task_state.py
        task_executor.py
        task_repository.py
        task_registry.py

    runtime/
        qt_executor.py
        cli_executor.py

    adapters/
        qt/
        cli/

domain/
    tasks/

ui/
    presenters/
    views/

app/
    main.py
```

---

# 15. Acceptance Criteria

* Domain task chạy được không cần Qt
* GUI và CLI dùng chung task
* Presenter test được độc lập
* Không circular dependency
* Không UI reference trong core

---

# 16. Future Extensions

* Task retry policy
* Task dependency (DAG)
* Logging system
* Metrics / tracing
* Plugin system

---

# 17. Summary

Framework này cung cấp:

* Task execution abstraction
* Multi-runtime support (Qt + CLI)
* Clean separation giữa Domain và UI
* Scalable architecture cho ứng dụng desktop chuyên nghiệp
