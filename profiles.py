"""Profile related functions."""

from typing import Dict, Any
from db import read_record_from_local_drive



def get_profile() -> Dict[str, Any]:
    """
    Retrieves the user profile from the local database.

    Returns:
        Dict[str, Any]: A dictionary containing the user's profile data,
                        including preferences and allergies.
    """
    return read_record_from_local_drive()
