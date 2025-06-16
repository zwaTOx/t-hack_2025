# app/bot.py
import asyncio
import logging
from pathlib import Path
import sys
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup, Update
import os
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.repositories.user import User, UserRepository
from app.database import Sessionlocal

load_dotenv()
BOT_TOKEN = os.getenv('BOT_API_KEY')

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
    application.add_handler(echo_handler)
    
    try:
        loop.run_until_complete(application.run_polling())
    finally:
        loop.close()