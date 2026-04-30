import pytest
from domain.types import TaskType, TaskStatus
from domain.tasks.download_factory import DownloadTaskFactory
from framework.core.registry import TaskRegistry
from framework.adapters.console.executor import ConsoleTaskExecutor
from framework.adapters.console.reporter import ConsoleProgressReporter

def test_domain_task_execution():
    factory = DownloadTaskFactory("http://test.com", "path")
    task = factory.create_task()
    reporter = ConsoleProgressReporter()
    executor = ConsoleTaskExecutor()

    status = executor.execute(task, reporter)
    assert status == TaskStatus.COMPLETED

def test_registry():
    registry = TaskRegistry()
    registry.register(TaskType.DOWNLOAD, DownloadTaskFactory)
    factory = registry.get_factory(TaskType.DOWNLOAD, "url", "path")
    assert isinstance(factory, DownloadTaskFactory)
