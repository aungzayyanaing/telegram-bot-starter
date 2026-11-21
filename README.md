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

## Commands

| Command | Who can use it | What it does |
| --- | --- | --- |
| `/start` | Anyone | Replies: "Hello! I'm a starter bot. Send /help to see what I can do." |
| `/help` | Anyone | Lists the available commands. |
| `/feedback` | Anyone | Starts a two-step conversation: the bot asks for your feedback, then forwards your next message to the admin. |
| `/cancel` | Anyone, during `/feedback` | Ends the feedback conversation. |
| `/broadcast <message>` | Admin only | Demo only: it does not send to any users. It replies "Broadcast ready to send to all users:" followed by the message. Without a message it replies "Usage: /broadcast <message>", and a non-admin gets "Sorry, only the admin can use /broadcast." |
| Any other text | Anyone | Echoes the message back as "You said: <your message>". |

## Configuration

| Setting | Required | What it is |
| --- | --- | --- |
| `BOT_TOKEN` | Yes | The token from @BotFather. If it is missing, the bot exits with: "BOT_TOKEN is missing. Copy .env.example to .env and fill it in." |
| `ADMIN_ID` | No | Your numeric Telegram user ID, from @userinfobot. It is used for `/broadcast` and for receiving forwarded feedback. The default in `.env.example` is `0`, which means no admin is set. A non-numeric value stops the bot at startup with an error message. |

## How feedback and broadcast work

- Feedback: if `ADMIN_ID` is set, the bot forwards the message to the admin as "New feedback from <name>:" followed by the message, and replies "Thanks! Your feedback has been sent." If no admin is set, or forwarding fails, it replies "Thanks! Your feedback has been recorded."
- Broadcast is a demo: there is no stored list of users, so it sends nothing to anyone; it only confirms the message as ready to send.
- The bot runs with long polling (`run_polling()` in `bot.py`); there is no webhook setup.

## What's not included

- No database and no stored list of users.
- No tests.
- No deployment or webhook configuration.

## Project structure

- `bot.py` — all handlers and the entry point
- `requirements.txt` — dependencies (`python-telegram-bot` 21.6 and `python-dotenv` 1.0.1, pinned)
- `.env.example` — config template

## License

MIT
