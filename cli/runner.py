import argparse
import uuid
import time
from framework.core.registry import TaskRegistry
from framework.core.repository import JsonTaskRepository
from framework.core.events import EventManager
from framework.runtime.cli_runtime import CLITaskExecutor
from framework.adapters.cli.progress_adapter import CLIProgressAdapter
from domain.tasks import register_domain_tasks

def main():
    register_domain_tasks()

    parser = argparse.ArgumentParser(description="CLI Task Runner")
    parser.add_argument("task_name", help="Name of the task to run", choices=TaskRegistry.list_tasks())
    args = parser.parse_args()

    repo = JsonTaskRepository("tasks.json")
    events = EventManager()

    def context_factory(task_id, repository, events, cancelled_set):
        return CLIProgressAdapter(task_id, repository, events, cancelled_set)

    executor = CLITaskExecutor(repo, events, context_factory)

    task_cls = TaskRegistry.get_task_class(args.task_name)
    task_id = str(uuid.uuid4())[:8]

    print(f"Starting task {args.task_name} (ID: {task_id})...")
    executor.execute(task_cls(), task_id, args.task_name)

    # Keep the main thread alive until the task is done
    while True:
        state = repo.get(task_id)
        if state and state.status.name in ["COMPLETED", "FAILED", "CANCELLED"]:
            print(f"Task finished with status: {state.status.name}")
            if state.result: print(f"Result: {state.result}")
            if state.error: print(f"Error: {state.error}")
            break
        time.sleep(0.5)

if __name__ == "__main__":
    main()
