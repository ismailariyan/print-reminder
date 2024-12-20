from datetime import datetime, timedelta


def check_reminders(data_manager, show_notification):
    data = data_manager.load_data()
    now = datetime.now()
    print("Checking for reminders...")

    for printer, info in data.items():
        last_print_date_str = info.get("last_print_date")
        last_notified_str = info.get("last_notified")

        if not last_print_date_str or last_print_date_str == "Not available":
            continue

        try:
            last_print_date = datetime.strptime(
                last_print_date_str, "%Y-%m-%d %H:%M:%S"
            )
        except ValueError:
            print(f"Invalid date format for printer {printer}")
            continue

        if last_notified_str and last_notified_str != "Not available":
            try:
                last_notified = datetime.strptime(
                    last_notified_str, "%Y-%m-%d %H:%M:%S"
                )
            except ValueError:
                last_notified = None
        else:
            last_notified = None

        interval_days = int(info.get("reminder_interval", 7))
        reminder_time = last_print_date + timedelta(days=interval_days)

        if now > reminder_time and (
            not last_notified or now > last_notified + timedelta(minutes=30)
        ):
            show_notification(
                title=f"Printer Reminder: {printer}",
                message=f"Your printer has not been used in the last {interval_days} days. Please print something!",
            )
            # print(f"Notification sent for printer {printer}")
            data[printer]["last_notified"] = now.strftime("%Y-%m-%d %H:%M:%S")
            data_manager.save_data(data)
