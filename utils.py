import sys
import os
import win32print


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def get_printer_list():
    printers = win32print.EnumPrinters(
        win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
    )
    return [printer[2] for printer in printers]


def setup_directories():
    app_directory = os.getenv("APPDATA")
    data_directory = os.path.join(app_directory, "Priminder")

    os.makedirs(data_directory, exist_ok=True)

    return data_directory
