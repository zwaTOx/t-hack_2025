import logging
from dotenv import load_dotenv
import os
from telegram import Bot
from telegram.error import TelegramError

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        self.bot_token = os.getenv('BOT_API_KEY')
        self.admin_chat_id = os.getenv('ADMIN_CHAT_ID')  
        self.bot = Bot(token=self.bot_token)

    async def send_code(self, code: str, chat_id: int, tg_id: str = None):
        try:
            message = f"🔑 Код для входа: {code}"
            if tg_id:
                message += f"\n👤 Для пользователя: {tg_id}"
            
            await self.bot.send_message(
                chat_id=chat_id,
                text=message
            )
            return True
        except TelegramError as e:
            logger.error(f"Ошибка отправки кода в Telegram: {e}")
            return False

telegram_bot = TelegramBot()