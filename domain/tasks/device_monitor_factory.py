from ..factory import TaskFactory
from .device_monitor_task import DeviceMonitorTask

class DeviceMonitorTaskFactory(TaskFactory):
    def __init__(self, device_id: str):
        self.device_id = device_id

    def create_task(self) -> DeviceMonitorTask:
        return DeviceMonitorTask(self.device_id)

    def build_title(self) -> str:
        return f"Device {self.device_id}"
