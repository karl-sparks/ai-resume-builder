"""Utility functions for the project."""

import json


def read_input(file_name: str) -> dict:
    """Read the input from the JSON file."""
    with open(file_name, encoding="utf-8") as json_file:
        data = json.load(json_file)
        return data

def add_data_to_json(file_path: str, new_data: dict) -> None:
    """Add new data to a JSON file."""
    # Step 1: Read existing JSON data from the file (if any)
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = {}  # If the file doesn't exist, start with an empty dictionary

    # Step 2: Modify the data structure (add new data)
    existing_data.update(new_data)

    # Step 3: Write the modified data back to the JSON file
    with open(file_path, 'w', encoding="utf-8") as file:
        json.dump(existing_data, file, indent=4)

    print("Data added to JSON file.")