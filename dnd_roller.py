"""
DnD Roller - A Discord bot for rolling dice and handling DnD combat mechanics.

This module serves as the main entry point for the Discord bot, initializing
the bot instance, loading cogs, and starting the connection to Discord.
"""

import os
from pathlib import Path

import discord
from discord.ext.commands import Bot

from lib.settings import DISCORD_TOKEN, PREFIX

# Directory containing cog extension modules
COGS_DIR: Path = Path("cogs")

# Enable all Discord intents for full functionality
INTENTS: discord.Intents = discord.Intents.all()

# Initialize the bot with command prefix and intents
bot: Bot = Bot(command_prefix=PREFIX, intents=INTENTS)


async def load_cogs() -> None:
    """
    Dynamically load all cog extensions from the 'cogs/' directory.

    Each Python file in the cogs directory is treated as an extension module
    that adds specific functionality to the bot (e.g., attack commands, dice rolling).

    Raises:
        ExtensionError: If a cog fails to load due to syntax or import errors.
    """
    print("Loading cogs...")

    # Iterate through all Python files in the cogs directory
    for filename in os.listdir(COGS_DIR):
        if filename.endswith(".py"):
            # Extract module name by removing .py extension
            module_name: str = filename[:-3]

            # Load the extension using dot notation (cogs.module_name)
            await bot.load_extension(f"cogs.{module_name}")
            print(f"  ✓ {module_name} loaded successfully")


@bot.event
async def on_ready() -> None:
    """
    Event handler called when the bot successfully connects to Discord.

    This function loads all cog extensions and prints a confirmation message
    indicating the bot is online and ready to receive commands.
    """
    await load_cogs()
    print(f"\n🎲 {bot.user} has connected to Discord and is ready!")


# Start the bot with the Discord token
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
