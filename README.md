# 🔊 Text-to-Speech Telegram Bot

A Telegram bot that converts text messages into audio using Microsoft Edge TTS. Supports multiple languages and voice genders with an intuitive inline button interface.

## Features

- 🌐 **7 languages** — English, Uzbek, Russian, French, Korean, Chinese, Turkish
- 👩👨 **Voice gender selection** — Female or Male for each language
- 📤 **Share button** — instantly share generated audio with anyone
- 🛡️ **Graceful error handling** — ignores photos, videos, stickers, and other non-text input
- ⚡ **Fast generation** — powered by Microsoft Edge TTS (free, no API key needed)

## Demo

```
User:  Hello, how are you?
Bot:   🌐 Choose a language:
       [🇺🇸 English] [🇺🇿 Uzbek] [🇷🇺 Russian]
       [🇫🇷 French]  [🇰🇷 Korean] [🇨🇳 Chinese] [🇹🇷 Turkish]

User:  [clicks English]
Bot:   ✅ Language: 🇺🇸 English
       👤 Now choose the voice gender:
       [👩 Female] [👨 Male]

User:  [clicks Female]
Bot:   🔊 [audio file] — with a 📤 Share button
```

## Supported Languages & Voices

| Language | Flag | Female Voice | Male Voice |
|----------|------|-------------|------------|
| English  | 🇺🇸 | en-US-AriaNeural | en-US-GuyNeural |
| Uzbek    | 🇺🇿 | uz-UZ-MadinaNeural | uz-UZ-SardorNeural |
| Russian  | 🇷🇺 | ru-RU-DariyaNeural | ru-RU-DmitryNeural |
| French   | 🇫🇷 | fr-FR-DeniseNeural | fr-FR-HenriNeural |
| Korean   | 🇰🇷 | ko-KR-SunHiNeural | ko-KR-InJoonNeural |
| Chinese  | 🇨🇳 | zh-CN-XiaoxiaoNeural | zh-CN-YunxiNeural |
| Turkish  | 🇹🇷 | tr-TR-EmelNeural | tr-TR-AhmetNeural |

## Installation

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/tts-bot.git
cd tts-bot
```

**2. Install dependencies**
```bash
pip install pyTelegramBotAPI edge-tts langdetect
```

**3. Set your bot token**

Open `main.py` and replace the token:
```python
bot = telebot.TeleBot(token="YOUR_BOT_TOKEN_HERE")
```

Or use an environment variable (recommended):
```python
import os
bot = telebot.TeleBot(token=os.environ.get("BOT_TOKEN"))
```

**4. Run the bot**
```bash
py main.py
```

## Getting a Bot Token

1. Open Telegram and message [@BotFather](https://t.me/BotFather)
2. Send `/newbot` and follow the steps
3. Copy the token and paste it into `main.py`
4. Enable **Inline Mode** in BotFather (required for the Share button):
   `/mybots` → select your bot → **Inline Mode** → turn on

## Project Structure

```
tts-bot/
├── main.py        
```

## Deployment

The bot can be hosted on any platform that supports Python:

- **Local machine** — just run `py main.py`
- **Railway** — connect GitHub repo, set `BOT_TOKEN` env variable, deploy
- **Render** — create a Background Worker service
- **Choreo** — add `BOT_TOKEN` in Manage Configs and Secrets

## Dependencies

| Package | Purpose |
|---------|---------|
| `pyTelegramBotAPI` | Telegram bot framework |
| `edge-tts` | Microsoft Edge TTS engine |
| `langdetect` | Auto language detection (optional) |

## License

MIT License — free to use, modify, and distribute.
