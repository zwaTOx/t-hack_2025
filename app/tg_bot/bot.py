# app/bot.py
import asyncio
from pathlib import Path
import sys
import time
import logging
from venv import logger
from dotenv import load_dotenv
# from openai import OpenAI
from telegram import ReplyKeyboardMarkup, Update, Voice
import os
# from pydub import AudioSegment
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
# from pydub.utils import which

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.repositories.user import User, UserRepository
from app.database import Sessionlocal

# ffmpeg_path = r"C:\Users\Пользователь\Downloads\ffmpeg-master-latest-win64-gpl\ffmpeg-master-latest-win64-gpl\bin"
# AudioSegment.ffmpeg = os.path.join(ffmpeg_path, "ffmpeg.exe")
# AudioSegment.ffprobe = os.path.join(ffmpeg_path, "ffprobe.exe")

load_dotenv()
BOT_TOKEN = os.getenv('BOT_API_KEY')
OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')

# try:
#     client = OpenAI(
#         api_key=OPENAI_API_KEY, base_url="https://api.openai.com/v1", timeout=60.0
#     )
#     logger.info("OpenAI client initialized successfully")
# except Exception as e:
#     logger.error(f"Failed to initialize OpenAI client: {e}")
#     raise

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
    keyboard = [
        ['Создать задачу', 'Показать все задачи']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await context.bot.send_message(chat_id=update.effective_chat.id, 
        text="Hi! I am alive. Click a button to proceed.", 
        reply_markup=reply_markup)

async def task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, 
        text="You have initiated a task creation. Please provide task details.")

async def view_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, 
        text="Here are all your tasks: ...")  

# async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     try:
#         voice: Voice = update.message.voice
#         chat_id = update.effective_chat.id

#         ogg_file = await context.bot.get_file(voice.file_id)
#         ogg_path = f"temp_{chat_id}.ogg"
#         await ogg_file.download_to_drive(ogg_path)

#         mp3_path = f"data/voice_msgs/temp_{chat_id}.mp3"
#         audio = AudioSegment.from_file(ogg_path, format="ogg")
#         audio.export(mp3_path, format="mp3")

#         with open(mp3_path, "rb") as audio_file:
#             transcript = client.audio.transcriptions.create(
#                 model="whisper-1",  
#                 file=audio_file,
#             )
#             texto = transcript.text
#             logger.info(f"Получена транскрипция: {texto}")

#         completion = client.chat.completions.create(
#             model="gpt-3.5-turbo",  
#             messages=[{"role": "user", "content": texto}],
#         )
#         response_text = completion.choices[0].message.content
#         logger.info(f"Сгенерированный ответ: {response_text}")

#         tts_response = client.audio.speech.create(
#             model="tts-1",  
#             voice="alloy",  
#             input=response_text,
#         )

#         tts_path = f"resp_{chat_id}.mp3"
#         tts_response.stream_to_file(tts_path)

#         ogg_resp_path = f"resp_{chat_id}.ogg"
#         audio_resp = AudioSegment.from_file(tts_path, format="mp3")
#         audio_resp.export(ogg_resp_path, format="ogg")

#         with open(ogg_resp_path, "rb") as resp:
#             await context.bot.send_voice(chat_id=chat_id, voice=resp)

#         for path in [ogg_path, mp3_path, tts_path, ogg_resp_path]:
#             try:
#                 os.remove(path)
#             except OSError as e:
#                 logger.warning(f"Не удалось удалить файл {path}: {e}")

#     except Exception as e:
#         logger.error(f"Ошибка в обработке голоса: {e}")
#         await update.message.reply_text(
#             "Извините, произошла ошибка при обработке вашего аудио."
#         )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == 'Создать задачу':
        await task(update, context)
    elif update.message.text == 'Показать все задачи':
        await view_tasks(update, context)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def start_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    task_handler = CommandHandler('task', task)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(start_handler)
    application.add_handler(task_handler)
    # application.add_handler(MessageHandler(filters.VOICE, voice_handler))
    application.add_handler(echo_handler)
    
    try:
        loop.run_until_complete(application.run_polling())
    finally:
        loop.close()