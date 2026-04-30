import sys
import os
import uuid
import time

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from framework.core.registry import TaskRegistry
from framework.core.repository import JsonTaskRepository
from framework.core.events import EventManager
from framework.runtime.cli_runtime import CLITaskExecutor
from framework.adapters.cli.progress_adapter import CLIProgressAdapter
from domain.tasks import register_domain_tasks

def main():
    register_domain_tasks()
    repo = JsonTaskRepository("batch_tasks.json")
    events = EventManager()

    def context_factory(task_id, repository, events, cancelled_set):
        return CLIProgressAdapter(task_id, repository, events, cancelled_set)

    executor = CLITaskExecutor(repo, events, context_factory)

    tasks_to_run = ["DemoTask", "LongRunningTask"]
    task_ids = []

    print("Queuing batch tasks...")
    for name in tasks_to_run:
        task_cls = TaskRegistry.get_task_class(name)
        tid = str(uuid.uuid4())[:8]
        task_ids.append(tid)
        executor.execute(task_cls(), tid, name)
        print(f"Queued {name} (ID: {tid})")

    while True:
        states = [repo.get(tid) for tid in task_ids]
        all_done = all(s.status.name in ["COMPLETED", "FAILED", "CANCELLED"] for s in states if s)
        if all_done:
            print("All tasks completed.")
            break
        time.sleep(1)

if __name__ == "__main__":
    main()
