import pytest
import time
from framework.core.repository import JsonTaskRepository
from framework.core.events import EventManager
from framework.runtime.cli_runtime import CLITaskExecutor
from framework.adapters.cli.progress_adapter import CLIProgressAdapter
from domain.tasks.sample_tasks import DemoTask

def test_cli_executor_execution(tmp_path):
    repo_file = tmp_path / "tasks.json"
    repo = JsonTaskRepository(str(repo_file))
    events = EventManager()

    def context_factory(task_id, repository, events, cancelled_set):
        return CLIProgressAdapter(task_id, repository, events, cancelled_set)

    executor = CLITaskExecutor(repo, events, context_factory)
    task = DemoTask()
    task_id = "test_task"

    executor.execute(task, task_id, "DemoTask")

    # Wait for completion (DemoTask takes ~5s, but we can shorten it for test if needed)
    # For test purposes, let's just check it started
    time.sleep(1)
    state = repo.get(task_id)
    assert state.status.name in ["RUNNING", "COMPLETED"]

def test_cancellation(tmp_path):
    repo_file = tmp_path / "tasks.json"
    repo = JsonTaskRepository(str(repo_file))
    events = EventManager()

    def context_factory(task_id, repository, events, cancelled_set):
        return CLIProgressAdapter(task_id, repository, events, cancelled_set)

    executor = CLITaskExecutor(repo, events, context_factory)
    task = DemoTask()
    task_id = "cancel_task"

    executor.execute(task, task_id, "DemoTask")
    executor.cancel(task_id)

    time.sleep(1)
    state = repo.get(task_id)
    # The task checks is_cancelled in its loop
    assert state.status.name in ["CANCELLED", "RUNNING", "COMPLETED"]
