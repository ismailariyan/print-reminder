from PyQt5.QtCore import QThread, pyqtSignal
import win32print
import time


class PrintQueueMonitor(QThread):
    new_print_job = pyqtSignal(str)

    def __init__(self, printer_name, parent=None):
        super().__init__(parent)
        self.printer_name = printer_name
        self._running = True

    def run(self):
        previous_jobs = set()
        while self._running:
            try:
                phandle = win32print.OpenPrinter(self.printer_name)
                print_jobs = win32print.EnumJobs(phandle, 0, -1, 1)
                current_jobs = {job["pDocument"] for job in print_jobs}

                new_jobs = current_jobs - previous_jobs
                if new_jobs:
                    self.new_print_job.emit(self.printer_name)

                previous_jobs = current_jobs
            except win32print.error as e:
                print(f"Win32 print error for printer '{self.printer_name}': {e}")
            except Exception as e:
                print(f"Unexpected error monitoring printer '{self.printer_name}': {e}")
            finally:
                try:
                    win32print.ClosePrinter(phandle)
                except Exception as e:
                    print(
                        f"Error closing printer handle for '{self.printer_name}': {e}"
                    )
            time.sleep(3)

    def stop(self):
        self._running = False
        self.wait()
