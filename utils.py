import sys
import os
import win32print
import win32com.client

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

def add_to_startup():
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
    app_path = os.path.abspath(sys.argv[0])
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(os.path.join(startup_folder, 'Priminder.lnk'))
    shortcut.Targetpath = app_path
    shortcut.WorkingDirectory = os.path.dirname(app_path)
    shortcut.IconLocation = os.path.join(os.path.dirname(app_path), 'resources', 'printer_icon.ico')
    shortcut.save()