from typing import Dict, Any
from domain.types import TaskType
from .executor import TaskExecutor
from .registry import TaskRegistry
from .store import TaskRuntimeStore

class TaskManager:
    def __init__(self, executor: TaskExecutor, registry: TaskRegistry, repository=None):
        self._executor = executor
        self._registry = registry
        self._repository = repository
        self._store = TaskRuntimeStore()
        # In a real app, this might be injected or handled by a factory
        self.view_factory = None
        self.presenter_factory = None

    def set_factories(self, view_factory, presenter_factory):
        self.view_factory = view_factory
        self.presenter_factory = presenter_factory

    def create_task(self, task_type: TaskType, *args, **kwargs):
        factory = self._registry.get_factory(task_type, *args, **kwargs)
        view = self.view_factory(factory.build_title())
        presenter = self.presenter_factory(view, factory, self)
        self._store.add(id(view), presenter)
        return view

    def bind_task(self, view, task_type: TaskType, *args, **kwargs):
        factory = self._registry.get_factory(task_type, *args, **kwargs)
        presenter = self._store.get(id(view))
        if not presenter:
            presenter = self.presenter_factory(view, factory, self)
            self._store.add(id(view), presenter)
        else:
            presenter.reconfigure(factory)
        return presenter

    def submit_runner(self, runner):
        # If the executor has a specialized runner submission (like Qt)
        if hasattr(self._executor, 'execute_runner'):
            self._executor.execute_runner(runner)
        else:
            # Fallback to standard execution
            self._executor.execute(runner.domain_task, runner.reporter)
