# Environment Variables Setup Guide

## Overview
The D&D Roller bot now uses environment variables to securely manage the Discord bot token. This prevents accidental exposure of sensitive credentials in version control.

## Setup Instructions

### Step 1: Create a `.env` File
Copy the `.env.example` file and rename it to `.env`:

```bash
cp .env.example .env
```

### Step 2: Add Your Discord Token
Edit the `.env` file and replace the placeholder with your actual bot token:

```
DISCORD_TOKEN=your_actual_discord_bot_token_here
```

### Step 3: Install Dependencies
Make sure python-dotenv is installed:

```bash
pip install -r requirements.txt
```

## How It Works

1. **`.env.example`** - This file shows users which environment variables they need to set. It's safe to commit to version control.

2. **`.env`** - This file contains your actual credentials and is **ignored by Git** (see `.gitignore`). Never commit this file!

3. **`lib/settings.py`** - Loads the `.env` file using `python-dotenv` and reads the `DISCORD_TOKEN` environment variable.

4. **Error Handling** - If the `DISCORD_TOKEN` is not set, the bot will raise a helpful error message before starting.

## Getting Your Discord Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name (e.g., "DnD Roller")
3. Go to the "Bot" section and click "Add Bot"
4. Under the TOKEN section, click "Copy"
5. Paste it into your `.env` file as `DISCORD_TOKEN=<your_token>`

## Security Best Practices

✅ **Do:**
- Keep your `.env` file private and never commit it
- Use environment variables for all secrets (tokens, API keys, etc.)
- Regenerate your token if you accidentally expose it
- Use `.env.example` as a template for other developers

❌ **Don't:**
- Commit `.env` files to version control
- Share your token with others
- Hardcode tokens in source files
- Push credentials to public repositories

## Alternative: System Environment Variables

If you prefer not to use a `.env` file, you can set the environment variable directly in your terminal:

```bash
# macOS/Linux
export DISCORD_TOKEN="your_token_here"
python dnd_roller.py

# Windows (PowerShell)
$env:DISCORD_TOKEN="your_token_here"
python dnd_roller.py

# Windows (Command Prompt)
set DISCORD_TOKEN=your_token_here
python dnd_roller.py
```

## Troubleshooting

**Error: "Discord token is not set"**
- Make sure you created the `.env` file
- Verify the token is correctly set as `DISCORD_TOKEN=...`
- Check that your `.env` file is in the project root directory

**Module not found: python-dotenv**
- Run `pip install -r requirements.txt`
- Or manually install: `pip install python-dotenv`
