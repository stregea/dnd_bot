"""
JSON file reading utilities for configuration management.

This module provides functions to read and validate JSON configuration files
used by the DnD Roller bot.
"""

import json
from pathlib import Path
from typing import Any


def read(json_config: str) -> dict[str, Any]:
    """
    Read a JSON file and return its contents as a dictionary.

    Args:
        json_config: Relative path to the JSON configuration file
                     from the current working directory.

    Returns:
        A dictionary containing the parsed JSON data.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        json.JSONDecodeError: If the file contains invalid JSON.

    Example:
        >>> config = read("config/config.json")
        >>> print(config["commands"]["prefix"])
        '!'
    """
    # Construct absolute path from current working directory
    json_path: Path = Path.cwd() / json_config

    # Open and parse the JSON file
    with json_path.open("r", encoding="utf-8") as file:
        data: dict[str, Any] = json.load(file)

    return data


def validate(config: dict[str, Any]) -> bool:
    """
    Validate that a configuration dictionary contains required fields.

    Args:
        config: The configuration dictionary to validate.

    Returns:
        True if the configuration is valid.

    Raises:
        ValueError: If required fields are missing or invalid.

    TODO:
        - Implement schema validation for config.json
        - Implement schema validation for creatures.json
        - Add custom validation rules for specific fields
    """
    # Placeholder for future validation logic
    required_keys: list[str] = ["api_tokens", "commands", "attacks"]

    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required configuration key: '{key}'")

    return True
