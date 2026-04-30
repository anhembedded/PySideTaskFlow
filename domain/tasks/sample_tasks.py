import time
from framework.core.interfaces import Task, TaskContext

class DemoTask(Task):
    def run(self, ctx: TaskContext):
        ctx.log("Starting DemoTask")
        for i in range(1, 11):
            if ctx.is_cancelled():
                ctx.log("DemoTask cancelled")
                return
            time.sleep(0.5)
            ctx.report_progress(i * 10)
        ctx.log("DemoTask finished")
        return "Success"

class LongRunningTask(Task):
    def run(self, ctx: TaskContext):
        ctx.log("Starting LongRunningTask")
        for i in range(1, 101):
            if ctx.is_cancelled():
                ctx.log("LongRunningTask cancelled")
                return
            time.sleep(0.1)
            ctx.report_progress(i)
        ctx.log("LongRunningTask finished")
        return "Done"

class DeviceMonitorTask(Task):
    def run(self, ctx: TaskContext):
        ctx.log("Monitoring device...")
        count = 0
        while not ctx.is_cancelled():
            time.sleep(1)
            count += 1
            ctx.log(f"Device update #{count}")
            # In a real monitor, progress might not be relevant or could be heartbeats
            ctx.report_progress(count % 101)
            if count >= 100: break # Just for safety in demo
        return f"Monitored {count} updates"
