# Telegram Bot Starter

A clean, minimal starter template for building Telegram bots with Python and [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) v21.

## Features

- `/start` and `/help` commands
- Echo replies for plain messages
- `/feedback` conversation (two steps, forwards the message to the admin)
- `/broadcast` admin-only command (demo version confirms the message instead of sending)
- Config via `.env`, structured logging

## Quick start

1. Talk to [@BotFather](https://t.me/BotFather) and create a bot to get a token.
2. Copy `.env.example` to `.env` and fill in `BOT_TOKEN` (and `ADMIN_ID`).
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python bot.py`

Get your own Telegram user ID from [@userinfobot](https://t.me/userinfobot) and put it in `ADMIN_ID`.

## Project structure

- `bot.py` — all handlers and the entry point
- `requirements.txt` — dependencies
- `.env.example` — config template

## License

MIT
