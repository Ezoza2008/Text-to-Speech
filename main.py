import telebot
import os
import asyncio
import edge_tts
from telebot import types

bot = telebot.TeleBot(token="8958790619:AAGRloCEKRk7oRplD4oBxeo5klz-gIaiNTE")

# Store user state: {user_id: {"text": ..., "lang": ...}}
user_state = {}

# Voice map: {lang_code: {"female": voice, "male": voice, "flag": emoji, "label": name}}
VOICES = {
    "en": {"female": "en-US-AriaNeural",    "male": "en-US-GuyNeural",      "flag": "🇺🇸", "label": "English"},
    "uz": {"female": "uz-UZ-MadinaNeural",  "male": "uz-UZ-SardorNeural",   "flag": "🇺🇿", "label": "Uzbek"},
    "ru": {"female": "ru-RU-DariyaNeural",  "male": "ru-RU-DmitryNeural",   "flag": "🇷🇺", "label": "Russian"},
    "fr": {"female": "fr-FR-DeniseNeural",  "male": "fr-FR-HenriNeural",    "flag": "🇫🇷", "label": "French"},
    "ko": {"female": "ko-KR-SunHiNeural",   "male": "ko-KR-InJoonNeural",   "flag": "🇰🇷", "label": "Korean"},
    "zh": {"female": "zh-CN-XiaoxiaoNeural","male": "zh-CN-YunxiNeural",    "flag": "🇨🇳", "label": "Chinese"},
    "tr": {"female": "tr-TR-EmelNeural",    "male": "tr-TR-AhmetNeural",    "flag": "🇹🇷", "label": "Turkish"},
}


def language_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton(f"{v['flag']} {v['label']}", callback_data=f"lang_{k}")
        for k, v in VOICES.items()
    ]
    markup.add(*buttons)
    return markup


def gender_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("👩 Female", callback_data="gender_female"),
        types.InlineKeyboardButton("👨 Male",   callback_data="gender_male"),
    )
    return markup


@bot.message_handler(commands=["start"])
def startcommand(message):
    bot.send_message(
        message.chat.id,
        "👋 Hi! Send me any text and I'll convert it to audio.\n\nJust type something to get started!"
    )


@bot.message_handler(content_types=["text"])
def receive_text(message):
    user_state[message.from_user.id] = {"text": message.text.strip()}
    bot.send_message(
        message.chat.id,
        "🌐 Choose a language for the voice:",
        reply_markup=language_keyboard()
    )


@bot.callback_query_handler(func=lambda c: c.data.startswith("lang_"))
def choose_language(call):
    lang = call.data.split("_")[1]
    uid = call.from_user.id

    if uid not in user_state:
        bot.answer_callback_query(call.id, "⚠️ Please send your text first.")
        return

    user_state[uid]["lang"] = lang
    label = VOICES[lang]["label"]
    flag = VOICES[lang]["flag"]

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"✅ Language: {flag} {label}\n\n👤 Now choose the voice gender:",
        reply_markup=gender_keyboard()
    )
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda c: c.data.startswith("gender_"))
def choose_gender(call):
    gender = call.data.split("_")[1]
    uid = call.from_user.id

    if uid not in user_state or "lang" not in user_state[uid]:
        bot.answer_callback_query(call.id, "⚠️ Please start over by sending your text.")
        return

    lang = user_state[uid]["lang"]
    text = user_state[uid]["text"]
    voice = VOICES[lang][gender]
    flag = VOICES[lang]["flag"]
    label = VOICES[lang]["label"]
    gender_emoji = "👩" if gender == "female" else "👨"

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"⏳ Generating audio...\n\n🌐 {flag} {label}  {gender_emoji} {gender.capitalize()}"
    )
    bot.answer_callback_query(call.id)

    filename = f"audio_{uid}.mp3"

    try:
        async def generate():
            communicate = edge_tts.Communicate(text, voice=voice)
            await communicate.save(filename)

        asyncio.run(generate())

        # Share button — forwards the audio to any chat
        share_markup = types.InlineKeyboardMarkup()
        share_markup.add(
            types.InlineKeyboardButton("📤 Share", switch_inline_query=text[:50])
        )

        with open(filename, "rb") as audio:
            bot.send_audio(
                call.message.chat.id,
                audio,
                title=f"{flag} {label} — {gender_emoji} {gender.capitalize()}",
                caption=f"🔊 Here's your audio!\n\n_{text[:100]}{'...' if len(text) > 100 else ''}_",
                parse_mode="Markdown",
                reply_markup=share_markup
            )

    except Exception as e:
        bot.send_message(call.message.chat.id, f"❌ Error generating audio: {e}")

    finally:
        if os.path.exists(filename):
            os.remove(filename)
        user_state.pop(uid, None)  # clean up state


@bot.message_handler(content_types=["photo", "video", "audio", "document", 
                                      "sticker", "voice", "video_note", 
                                      "location", "contact", "animation"])
def handle_unsupported(message):
    bot.reply_to(message, "✍️ Please send me a text message only — I'll convert it to audio for you!")


bot.polling()