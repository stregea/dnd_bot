# 🎲 DnD Roller Bot

A Discord bot for rolling dice and handling DnD 5e combat mechanics. Automate attack rolls for multiple creatures with support for advantage, disadvantage, critical hits, and damage calculation.

---

## 📋 Table of Contents

- [Features](#-features)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Commands](#-commands)
- [Adding Creatures](#-adding-creatures)
- [Project Structure](#-project-structure)

---

## ✨ Features

- **Multi-creature attacks** - Roll attacks for multiple creatures at once
- **Attack types** - Support for standard, advantage, and disadvantage rolls
- **Critical hits & misses** - Automatic detection and damage calculation
- **Customizable creatures** - Define creatures and their actions in JSON
- **Damage breakdown** - Detailed roll information for each attack

---

## 📦 Requirements

- **Python 3.12+** (required for modern type syntax)
- **Discord Bot Token** ([Create one here](https://discord.com/developers/applications))

---

## 🚀 Installation

### Prerequisites

1. **Install Python 3.12 or later:**
   - **macOS:** `brew install python@3.12` or [download from python.org](https://python.org)
   - **Windows:** [Download from python.org](https://python.org) (check "Add Python to PATH")
   - **Linux:** `sudo apt install python3.12` or use your package manager

2. **Create a Discord Bot:**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application
   - Go to **Bot** → **Add Bot**
   - Copy the **Token** (you'll need this later)
   - Enable **Privileged Gateway Intents** (Presence, Server Members, Message Content)
   - Go to **OAuth2** → **URL Generator**, select `bot` scope, choose permissions
   - Use the generated URL to invite the bot to your server

### Quick Start

#### macOS / Linux

```bash
# Clone or download the project
cd /path/to/DnD

# Run the startup script
./start.sh
```

#### Windows

```batch
# Double-click start.bat in File Explorer
# Or run from Command Prompt:
start.bat
```

The startup scripts will automatically:
1. Create a virtual environment (if needed)
2. Install dependencies
3. Start the bot

---

## ⚙️ Configuration

### Environment Variables Setup

The D&D Roller bot uses environment variables to securely manage the Discord bot token. This prevents accidental exposure of sensitive credentials in version control.

#### Step 1: Create a `.env` File

Copy the `.env.example` file and rename it to `.env`:

```bash
cp .env.example .env
```

#### Step 2: Add Your Discord Token

Edit the `.env` file in the `config/` directory and replace the placeholder with your actual bot token:

```
DISCORD_TOKEN=your_actual_discord_bot_token_here
```

#### Step 3: Install Dependencies

Make sure all dependencies are installed:

```bash
pip install -r requirements.txt
```

### Getting Your Discord Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name (e.g., "DnD Roller")
3. Go to the "Bot" section and click "Add Bot"
4. Under the TOKEN section, click "Copy"
5. Paste it into your `config/.env` file as `DISCORD_TOKEN=<your_token>`

### Other Configuration

Edit `config/config.json` for command settings:

```json
{
  "commands": {
    "prefix": "!",
    "roll": "roll"
  },
  "attacks": {
    "standard": "standard",
    "advantage": "advantage",
    "disadvantage": "disadvantage"
  }
}
```


---

## 🎮 Usage

Once the bot is running and connected to your Discord server, use commands in any text channel where the bot has permissions.

---

## 📝 Commands

### Attack Command

Roll attacks for multiple creatures against a target.

```
!attack <creature> <count> <target_ac> [attack_type] [action]
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `creature` | string | ✅ | Creature name (use quotes for multi-word names) |
| `count` | number | ✅ | Number of creatures attacking |
| `target_ac` | number | ✅ | Target's armor class |
| `attack_type` | string | ❌ | `standard`, `advantage`, or `disadvantage` (default: `standard`) |
| `action` | string | ❌ | Specific action name (default: creature's default action) |

**Examples:**

```
!attack wolf 3 15
!attack wolf 5 14 advantage
!attack wolf 2 16 disadvantage
!attack "dire wolf" 4 15 standard bite
```

**Output:**

The bot responds with an embed showing:
- Each attack roll (with dice breakdown for advantage/disadvantage)
- Hit/miss status
- Critical hits and critical failures
- Damage for each hit
- Summary of total hits and damage

---

## 🐺 Adding Creatures

Define creatures in `config/creatures.json`:

```json
{
  "wolf": {
    "default_action": "bite",
    "actions": {
      "bite": {
        "attack_bonus": 4,
        "damage": {
          "count": 2,
          "sides": 4,
          "bonus": 2
        }
      }
    }
  },
  "goblin": {
    "default_action": "scimitar",
    "actions": {
      "scimitar": {
        "attack_bonus": 4,
        "damage": {
          "count": 1,
          "sides": 6,
          "bonus": 2
        }
      },
      "shortbow": {
        "attack_bonus": 4,
        "damage": {
          "count": 1,
          "sides": 6,
          "bonus": 2
        }
      }
    }
  }
}
```

**Structure:**

- `default_action`: The action used when none is specified
- `actions`: Dictionary of available actions
  - `attack_bonus`: Added to the d20 roll
  - `damage`:
    - `count`: Number of damage dice
    - `sides`: Die type (4 = d4, 6 = d6, etc.)
    - `bonus`: Flat damage bonus

---

## 📁 Project Structure

```
DnD/
├── dnd_roller.py               # Main bot entry point
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .gitignore                  # Git ignore rules
├── start.sh                    # macOS/Linux startup script
├── start.bat                   # Windows startup script
├── cogs/
│   └── attack.py               # Attack command cog
├── config/
│   ├── .env.example            # Environment variables template (copy to .env)
│   ├── config.json             # Bot configuration
│   └── creatures.json          # Creature definitions
└── lib/
    ├── json_reader.py          # JSON file utilities
    ├── roll.py                 # Dice rolling functions
    └── settings.py             # Configuration loader & .env file reader
```

**Key Files:**
- **`.env.example`** - Template for environment variables (copy to `.env` and fill in your Discord token).
- **`.env`** - Contains your Discord bot token (created by user, not included in repo).
- **`config.json`** - Bot command settings and prefixes.
- **`creatures.json`** - Creature definitions with attacks and damage rolls.

