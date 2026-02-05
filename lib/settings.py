"""
Settings module for DnD Roller bot configuration.

This module loads configuration values from JSON files and environment variables,
exposing them as typed constants for use throughout the application.
"""

import os
from typing import Any

from dotenv import load_dotenv

from lib.json_reader import read

# Load environment variables from .env file
load_dotenv(dotenv_path="config/.env")

# Type alias for configuration dictionaries
ConfigDict = dict[str, Any]

# Load configuration files
CONFIG: ConfigDict = read("config/config.json")
CREATURES: ConfigDict = read("config/creatures.json")

# Discord API settings - Read from environment variable
DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN", "")

# Command configuration
PREFIX: str = CONFIG["commands"]["prefix"]
ROLL_COMMAND: str = CONFIG["commands"]["roll"]

# Attack type command identifiers
STANDARD_ATTACK_COMMAND: str = CONFIG["attacks"]["standard"]
ADVANTAGE_ATTACK_COMMAND: str = CONFIG["attacks"]["advantage"]
DISADVANTAGE_ATTACK_COMMAND: str = CONFIG["attacks"]["disadvantage"]

# Validate required configuration
if not DISCORD_TOKEN:
    raise RuntimeError(
        "Discord token is not set. Please set the DISCORD_TOKEN environment variable "
        "or add it to a .env file. See .env.example for more information."
    )
