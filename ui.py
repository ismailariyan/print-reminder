from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QSystemTrayIcon,
    QMenu,
    QAction,
    QMessageBox,
    QApplication,
)
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from data_manager import DataManager
from printer_queue_monitor import PrintQueueMonitor
from datetime import datetime, timedelta
from utils import get_printer_list
from reminder_checker import check_reminders


class PrintReminderGUI(QWidget):
    def __init__(self, icon_path, data_directory):
        super().__init__()
        self.setWindowTitle("Print Reminder")
        self.setWindowIcon(QIcon(icon_path))
        self.resize(400, 300)

        self.tray_icon = QSystemTrayIcon(QIcon(icon_path), self)
        self.tray_icon.setToolTip("Print Reminder")
        tray_menu = QMenu()

        restore_action = QAction("Open", self)
        restore_action.triggered.connect(self.show_normal)
        tray_menu.addAction(restore_action)

        exit_action = QAction("Close", self)
        exit_action.triggered.connect(self.exit_app)
        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

        self.tray_icon.messageClicked.connect(self.show_normal)

        self.data_manager = DataManager(data_directory)
        self.data = self.data_manager.load_data()

        self.init_ui()

        self.reminder_timer = QTimer(self)
        self.reminder_timer.timeout.connect(self.check_reminders)
        self.reminder_timer.start(600000)  # 10 mins in milliseconds

        self.monitors = []
        self.start_monitoring()

        self.tray_icon.show()

    def init_ui(self):
        layout = QVBoxLayout()

        self.setStyleSheet(
            """
            QWidget {
                background-color: #2E3440;
                color: #D8DEE9;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            QLabel {
                font-weight: bold;
            }
            QComboBox, QCheckBox {
                background-color: #3B4252;
                border: 1px solid #434C5E;
                padding: 5px;
            }
            QPushButton {
                background-color: #81A1C1;
                border: none;
                padding: 10px;
                color: #2E3440;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #88C0D0;
            }
        """
        )

        self.label_printer = QLabel("Select Printer:")
        layout.addWidget(self.label_printer)

        self.printer_dropdown = QComboBox()
        self.printer_dropdown.addItems(get_printer_list())
        self.printer_dropdown.currentIndexChanged.connect(self.update_last_print_date)
        layout.addWidget(self.printer_dropdown)

        self.label_last_print = QLabel("Last Print Date: ")
        layout.addWidget(self.label_last_print)

        self.label_interval = QLabel("Reminder Interval (Days):")
        layout.addWidget(self.label_interval)

        self.interval_dropdown = QComboBox()
        self.interval_dropdown.addItems(["1", "7", "14", "21", "30"])
        layout.addWidget(self.interval_dropdown)

        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)

        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

        self.update_last_print_date()

    def update_last_print_date(self):
        printer_name = self.printer_dropdown.currentText()
        if printer_name:
            if printer_name in self.data:
                last_print_date_str = self.data[printer_name].get(
                    "last_print_date", "Not available"
                )
                if last_print_date_str != "Not available":
                    try:
                        last_print_date = datetime.strptime(
                            last_print_date_str, "%Y-%m-%d %H:%M:%S"
                        )
                        self.label_last_print.setText(
                            f"Last Print Date: {last_print_date.strftime('%Y-%m-%d %H:%M:%S')}"
                        )
                    except ValueError:
                        self.label_last_print.setText("Last Print Date: Invalid format")
                else:
                    self.label_last_print.setText("Last Print Date: Not available")

                # Load settings for interval and short reminder
                interval = self.data[printer_name].get("reminder_interval", "7")
                index = self.interval_dropdown.findText(str(interval))
                if index != -1:
                    self.interval_dropdown.setCurrentIndex(index)
            else:
                self.label_last_print.setText("Last Print Date: Not available")
                self.interval_dropdown.setCurrentIndex(0)
        else:
            self.label_last_print.setText("Last Print Date:")

    def save_settings(self):
        printer_name = self.printer_dropdown.currentText()
        reminder_interval = self.interval_dropdown.currentText()
        if printer_name:
            if printer_name not in self.data:
                self.data[printer_name] = {
                    "last_print_date": "Not available",
                    "reminder_interval": reminder_interval,
                    "last_notified": "Not available",
                }
            else:
                self.data[printer_name]["reminder_interval"] = reminder_interval
            self.data_manager.save_data(self.data)
            self.status_label.setText(f"Settings saved for {printer_name}")
            QMessageBox.information(
                self,
                "Settings Saved",
                f"Settings have been saved for printer: {printer_name}",
            )
        else:
            QMessageBox.warning(
                self, "No Printer Selected", "Please select a printer to save settings."
            )

    def check_reminders(self):
        check_reminders(self.data_manager, self.show_notification)

    def show_notification(self, title, message=None):
        if message is None:
            message = ""
        self.tray_icon.showMessage(title, message, QSystemTrayIcon.Information, 10000)

    def start_monitoring(self):
        printers = get_printer_list()
        for printer in printers:
            monitor = PrintQueueMonitor(printer)
            monitor.new_print_job.connect(self.handle_new_print_job)
            monitor.start()
            self.monitors.append(monitor)

    def handle_new_print_job(self, printer_name):
        now = datetime.now()
        if printer_name not in self.data:
            self.data[printer_name] = {
                "last_print_date": "Not available",
                "reminder_interval": "7",
                "last_notified": "Not available",
            }
        self.data[printer_name]["last_print_date"] = now.strftime("%Y-%m-%d %H:%M:%S")
        self.data[printer_name]["last_notified"] = "Not available"
        self.data_manager.save_data(self.data)
        self.update_last_print_date()

        self.show_notification(
            title=f"New Print Job Detected: {printer_name}",
            message=f"A new print job has been sent to {printer_name}.",
        )

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "Print Reminder",
            "Application was minimized to Tray.",
            QSystemTrayIcon.Information,
            2000,
        )

    def show_normal(self):
        self.show()
        self.raise_()
        self.activateWindow()

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.show_normal()

    def exit_app(self):
        for monitor in self.monitors:
            monitor.stop()
        QApplication.quit()
