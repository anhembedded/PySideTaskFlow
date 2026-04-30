import time
from ..base_task import DomainTask
from ..interfaces import ProgressReporter

class DeviceMonitorTask(DomainTask):
    def __init__(self, device_id: str):
        super().__init__(f"Monitor: {device_id}")
        self.device_id = device_id

    def execute(self, reporter: ProgressReporter):
        reporter.report_message(f"Starting monitor for {self.device_id}")
        count = 0
        while not reporter.is_cancelled():
            count += 1
            reporter.report_message(f"Heartbeat {count} from {self.device_id}")
            reporter.report_progress(count % 101)
            time.sleep(1)
            if count >= 10: break # Demo limit
        reporter.report_message("Monitoring session finished")
