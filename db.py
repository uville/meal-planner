"""Handle data-related logic."""

import os
import json
from typing import Dict

DB_FILEPATH = "db.json"


def read_record_from_local_drive() -> Dict[str, str]:
    """
    Reads a record from the local JSON database file.

    Returns:
        Dict[str, str]: A dictionary containing preferences and allergies,
                        or an empty dictionary if the file does not exist.
    """
    if os.path.exists(DB_FILEPATH):
        with open(DB_FILEPATH, "r", encoding="utf8") as file:
            return json.load(file)
    return {}


def write_record_to_local_drive(preferences: str, allergies: str) -> Dict[str, str]:
    """
    Saves preferences and allergies to the local JSON database file.

    Args:
        preferences (str): The user's preferences.
        allergies (str): The user's allergies.

    Returns:
        Dict[str, str]: A dictionary containing the saved preferences and allergies.
    """
    record = {"preferences": preferences, "allergies": allergies}
    with open(DB_FILEPATH, "w", encoding="utf8") as file:
        json.dump(record, file)
    return record
