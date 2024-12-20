import sys
import os
from PyQt5.QtWidgets import QApplication
from ui import PrintReminderGUI
from utils import resource_path, setup_directories


def main():
    data_directory = setup_directories()
    icon_path = resource_path(os.path.join("resources", "printer_icon.png"))

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = PrintReminderGUI(icon_path, data_directory)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
