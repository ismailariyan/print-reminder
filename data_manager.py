import os
import json


class DataManager:
    def __init__(self, data_directory):
        self.database_file = os.path.join(data_directory, "data.json")
        self.setup_database()

    def setup_database(self):
        os.makedirs(os.path.dirname(self.database_file), exist_ok=True)
        if not os.path.exists(self.database_file):
            with open(self.database_file, "w") as file:
                json.dump({}, file)

    def load_data(self):
        try:
            with open(self.database_file, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_data(self, data):
        with open(self.database_file, "w") as file:
            json.dump(data, file, indent=4)
