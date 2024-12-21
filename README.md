# Print Reminder

A desktop application that monitors printers and sends reminders if they haven't been used for a specified period. This prevents ink drying or mechanical failures caused by prolonged inactivity.

## Table of Contents
- [Set Reminder Interval](#set-reminder-interval)
  - [Notifications](#notifications)
- [Usage](#usage)
- [Demo](#demo)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## About This Project

Print Reminder is a Windows-only desktop application designed to help users keep their printers active and in good working condition. By monitoring printer usage and sending timely reminders, it ensures that printers are regularly used, preventing issues such as ink drying or mechanical failures due to prolonged inactivity.

## Features

### Printer List and Last Print Date

- **Display Available Printers:** Retrieves and displays a list of available printers using.
- **Show Last Print Date:** Displays the last print date for the selected printer.

### Set Reminder Interval

- **Reminder Options:** Choose the reminder interval from a dropdown menu:
  - Choose the interval starting from 1, 7, 14, 21, 30 days.

### Notifications

- **Periodic Check:** Regularly checks if the printer hasn't been used within the set interval.
- **Desktop Notifications:** Sends a desktop notification to remind the user to print.

## Usage

1. **Select Printer:** Choose your printer from the list of available printers.
2. **Set Interval:** Select the reminder interval from the dropdown menu.
3. **Save Settings:** Confirm your choices to store them in the application.
4. **Receive Notifications:** You will get alerts when your printer hasn’t been used within the specified time.

## Demo

![Print Reminder Demo](https://github.com/ismailariyan/print-reminder/blob/832e68c681b391eb15edcd83ba014c0090dd3d1e/resources/demo.gif)

*Example of the Print Reminder application in action.*
## Technologies Used

- **Python**
- **PyQt5** for the GUI
- **win32print** for printer interactions on Windows
- **plyer** for desktop notifications

## Installation Guide

Follow these steps to set up and run the Print Reminder application on Windows.
```bash
   git clone https://github.com/yourusername/print-reminder.git
   cd print-reminder
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   python main.py   
```
If you wish th build the .exe yourself
```bash
    python -m PyInstaller main.spec
```
## Contributing

Contributions are welcome to make Print Reminder even better. To contribute:
1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m "Add a new feature"`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
