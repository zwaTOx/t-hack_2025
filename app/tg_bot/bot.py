# app/bot.py
import asyncio
import logging
import os
from pathlib import Path
import sys
from dotenv import load_dotenv
from faster_whisper import WhisperModel
from telegram import ReplyKeyboardMarkup, Update, Voice
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from app.tg_bot.telegram_bot_model import TelegramBot
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.repositories.user import User, UserRepository
from app.database import Sessionlocal

load_dotenv()
BOT_TOKEN = os.getenv('BOT_API_KEY')
logger = logging.getLogger(__name__)

try:
    model = WhisperModel("small", device="cpu", compute_type="int8")
    logger.info("Whisper model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load Whisper model: {e}")
    raise

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    tg_id = update.effective_user.username  
    with Sessionlocal() as db:
        user_repo = UserRepository(db)
        user = user_repo.create_user(
            tg_id=f"@{tg_id}" if tg_id else str(update.effective_user.id),
            chat_id=chat_id
        )
    keyboard = [['Создать задачу', 'Показать все задачи']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="""🚀 Привет, я — твой AI-ассистент!
Моя суперсила — превращать твои слова в задачи. Просто скажи:
«Добавь “Выучить Python” в список целей»
«Напомни выгулять кота в 18:00»
Голосом работает тоже! Попробуй нажать 🎤 😉""", 
        reply_markup=reply_markup
    )

async def task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Опишите задачу текстом."
    )

async def view_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Список задач:\n1. Пример задачи 1\n2. Пример задачи 2"
    )

async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ogg_path = None
    try:
        voice = update.message.voice
        chat_id = update.effective_chat.id

        voice_file = await context.bot.get_file(voice.file_id)
        ogg_path = f"temp_{chat_id}.ogg"
        await voice_file.download_to_drive(ogg_path)

        segments, info = model.transcribe(
            ogg_path,
            language="ru",  
            beam_size=5,
            vad_filter=True  
        )
        
        texto = " ".join([segment.text for segment in segments])
        logger.info(f"Detected language: {info.language}, probability: {info.language_probability}")
        logger.info(f"Получена транскрипция: {texto}")
        
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"🔊 Распознанный текст:\n{texto}"
        )

        await TelegramBot().send_msg_on_n8n(
            chat_id=update.effective_chat.id,
            msg=texto+f' [{update.message.date}]'
        )

    except Exception as e:
        logger.error(f"Ошибка в обработке голоса: {e}")
        await update.message.reply_text(
            "⚠️ Не удалось обработать голосовое сообщение"
        )
    finally:
        if ogg_path and os.path.exists(ogg_path):
            try:
                os.remove(ogg_path)
            except Exception as e:
                logger.warning(f"Не удалось удалить файл {ogg_path}: {e}")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == 'Создать задачу':
        await task(update, context)
    elif text == 'Показать все задачи':
        await view_tasks(update, context)
    else:
        await TelegramBot().send_msg_on_n8n(
            chat_id=update.effective_chat.id,
            msg=text+f' [{update.message.date}]'
        )

def start_bot():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        application = ApplicationBuilder().token(BOT_TOKEN).build()
        application.add_handler(CommandHandler('start', start))
        application.add_handler(CommandHandler('task', task))
        application.add_handler(MessageHandler(filters.VOICE, voice_handler))
        application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))
        
        application.run_polling()
    except Exception as e:
        logger.error(f"Error in bot: {e}")
    finally:
        loop.close()

if __name__ == '__main__':
    start_bot()