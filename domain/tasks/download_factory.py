from ..factory import TaskFactory
from .download_task import DownloadTask

class DownloadTaskFactory(TaskFactory):
    def __init__(self, url: str, save_path: str):
        self.url = url
        self.save_path = save_path

    def create_task(self) -> DownloadTask:
        return DownloadTask(self.url, self.save_path)

    def build_title(self) -> str:
        return f"Downloading {self.url}"
