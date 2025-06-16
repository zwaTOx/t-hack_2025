from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

import uvicorn
import asyncio
from threading import Thread
from app.tg_bot.bot import start_bot

def run_bot():
    start_bot()

def run_fastapi():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)

if __name__ == "__main__":

    bot_thread = Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    run_fastapi()