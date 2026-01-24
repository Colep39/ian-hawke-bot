# Ian Hawke — Discord Class Bot

Ian Hawke is a custom Discord bot designed for **class and academic Discord servers**.  
It provides anonymous announcements, keyword-based responses, and automated reactions to help streamline communication and add personality to class servers.

Built using **Python** and **discord.py**, the bot is lightweight, secure, and easy to extend.

---

## Features

- **Anonymous `/say` Slash Command**
  - Allows admins to make the bot send messages to any channel
  - No attribution — users do not see who issued the command
- **Keyword Detection**
  - Watches chat messages for specific keywords
  - Automatically responds with messages or GIFs
- **User-Specific Watching**
  - Optionally react only to messages from specific users
- **Admin-Only Controls**
  - Sensitive commands can be restricted to administrators
- **Secure Token Handling**
  - Uses environment variables (`.env`) for safety

---

## Tech Stack

- **Language:** Python 3.10+
- **Discord API:** discord.py
- **Environment Management:** python-dotenv

---

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ian-hawke-bot.git
cd ian-hawke-bot
```

### 2. Create a Python Virutal Environment
```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variable
```bash
DISCORD_TOKEN=your_bot_token_here
```

## Running the Bot:
```bash
python bot.py
```
If successful, it should say "Logged in as discord_bot_name"

## License

```text
Personal Use License

Copyright (c) 2026 Cole Plagens

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to use
the Software for personal and educational purposes only, subject to the
following conditions:

- The Software may be used, modified, and run for personal or academic Discord servers.
- The Software may be forked or cloned for learning and non-commercial purposes.

The following actions are NOT permitted without explicit written permission:
- Selling, sublicensing, or distributing the Software or derivative works
- Using the Software for commercial purposes
- Hosting the Software as a paid service

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
