import json
import logging
import os

DEFAULT_PATH = "data/gradebook.json"


def load_data(path=DEFAULT_PATH):
    """Load gradebook data from a JSON file."""
    try:
        if not os.path.exists(path):
            logging.info("Data file not found. Starting with empty data.")
            return {}

        with open(path, "r") as file:
            data = json.load(file)
            logging.info("Data loaded successfully from %s", path)
            return data

    except FileNotFoundError:
        logging.error("File not found: %s", path)
        return {}

    except json.JSONDecodeError:
        logging.error("Invalid JSON in %s", path)
        return {}

    except Exception as e:
        logging.error("Unexpected error while loading data: %s", e)
        return {}


def save_data(data, path=DEFAULT_PATH):
    """Save gradebook data to a JSON file."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w") as file:
            json.dump(data, file, indent=4)

        logging.info("Data saved successfully to %s", path)

    except Exception as e:
        logging.error("Error while saving data: %s", e)