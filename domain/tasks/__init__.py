from framework.core.registry import TaskRegistry
from .sample_tasks import DemoTask, LongRunningTask, DeviceMonitorTask

def register_domain_tasks():
    TaskRegistry.register("DemoTask", DemoTask)
    TaskRegistry.register("LongRunningTask", LongRunningTask)
    TaskRegistry.register("DeviceMonitorTask", DeviceMonitorTask)
