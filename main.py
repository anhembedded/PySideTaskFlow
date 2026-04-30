import sys
import os

# Dispatcher for the examples
def main():
    print("Select an application to run:")
    print("1. Task Dashboard (GUI)")
    print("2. Device Monitor (GUI)")
    print("3. Batch Runner (CLI)")
    print("4. CLI Runner (Dynamic)")

    choice = input("Enter choice (1-4): ")

    if choice == '1':
        os.system("python3 apps/task_dashboard/main.py")
    elif choice == '2':
        os.system("python3 apps/device_monitor/main.py")
    elif choice == '3':
        os.system("python3 apps/batch_runner/main.py")
    elif choice == '4':
        task = input("Enter task name (DemoTask, LongRunningTask, DeviceMonitorTask): ")
        os.system(f"python3 cli/runner.py {task}")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
