import sys
import argparse
from domain.types import TaskType
from domain.tasks.download_factory import DownloadTaskFactory
from domain.tasks.device_monitor_factory import DeviceMonitorTaskFactory
from framework.core.registry import TaskRegistry
from framework.core.manager import TaskManager
from framework.adapters.console.executor import ConsoleTaskExecutor
from framework.adapters.console.reporter import ConsoleProgressReporter

def main():
    registry = TaskRegistry()
    registry.register(TaskType.DOWNLOAD, DownloadTaskFactory)
    registry.register(TaskType.DEMO, DeviceMonitorTaskFactory)

    executor = ConsoleTaskExecutor()
    manager = TaskManager(executor, registry)

    parser = argparse.ArgumentParser(description="CLI Task Batch Runner")
    parser.add_argument("--tasks", nargs="+", help="Types of tasks to run (DOWNLOAD, DEMO)", default=["DOWNLOAD", "DEMO"])
    args = parser.parse_args()

    print(f"CLI Batch Runner starting {len(args.tasks)} tasks...")

    for t_name in args.tasks:
        try:
            t_type = TaskType[t_name.upper()]
            if t_type == TaskType.DOWNLOAD:
                factory = registry.get_factory(t_type, "http://example.com", "/tmp/cli")
            else:
                factory = registry.get_factory(t_type, "DEV-001")

            task = factory.create_task()
            reporter = ConsoleProgressReporter()
            print(f"\n--- Executing {task.name} ---")
            executor.execute(task, reporter)
        except KeyError:
            print(f"Unknown task type: {t_name}")

if __name__ == "__main__":
    main()
