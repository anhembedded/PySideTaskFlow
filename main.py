import os
import sys

def main():
    print("Task Framework Examples")
    print("1. GUI Application (PySide6)")
    print("2. CLI Application")

    choice = input("Select (1-2): ")
    if choice == '1':
        os.system("PYTHONPATH=. python3 apps/gui/main.py")
    elif choice == '2':
        os.system("PYTHONPATH=. python3 apps/cli/main.py")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
