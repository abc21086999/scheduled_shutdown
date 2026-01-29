import sys
from PySide6.QtWidgets import QApplication
from core.shutdown_manager import ShutdownManager
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)

    # Instantiate the logic manager
    manager = ShutdownManager()

    # Instantiate the UI, injecting the manager
    window = MainWindow(manager)
    window.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()
