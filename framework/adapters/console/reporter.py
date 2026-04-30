from domain.interfaces import ProgressReporter

class ConsoleProgressReporter(ProgressReporter):
    def report_progress(self, percent: int):
        print(f"Progress: {percent}%")

    def report_message(self, message: str):
        print(f"MSG: {message}")

    def is_cancelled(self) -> bool:
        return False # CLI cancellation usually handled via signals/interrupts
