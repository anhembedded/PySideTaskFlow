import pytest
import os
from framework.core.status import TaskStatus
from framework.core.state import TaskState
from framework.core.repository import JsonTaskRepository
from framework.core.events import EventManager
from framework.core.registry import TaskRegistry
from domain.tasks.sample_tasks import DemoTask

def test_task_state():
    state = TaskState(task_id="1", name="Test")
    assert state.status == TaskStatus.PENDING
    assert state.progress == 0

def test_json_repository(tmp_path):
    repo_file = tmp_path / "tasks.json"
    repo = JsonTaskRepository(str(repo_file))
    state = TaskState(task_id="1", name="Test")
    repo.save(state)

    loaded = repo.get("1")
    assert loaded.name == "Test"
    assert loaded.status == TaskStatus.PENDING

def test_event_manager():
    events = EventManager()
    received = []
    events.subscribe("test_event", lambda data: received.append(data))
    events.emit("test_event", "hello")
    assert received == ["hello"]

def test_task_registry():
    TaskRegistry.register("Demo", DemoTask)
    assert TaskRegistry.get_task_class("Demo") == DemoTask
    assert "Demo" in TaskRegistry.list_tasks()
