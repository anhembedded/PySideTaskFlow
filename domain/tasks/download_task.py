import time
from ..base_task import DomainTask
from ..interfaces import ProgressReporter

class DownloadTask(DomainTask):
    def __init__(self, url: str, save_path: str):
        super().__init__(f"Download: {url}")
        self.url = url
        self.save_path = save_path

    def execute(self, reporter: ProgressReporter):
        reporter.report_message(f"Starting download from {self.url}")
        for i in range(1, 101):
            if reporter.is_cancelled():
                reporter.report_message("Download cancelled")
                return
            time.sleep(0.05)  # Simulate download
            reporter.report_progress(i)
        reporter.report_message(f"Saved to {self.save_path}")
