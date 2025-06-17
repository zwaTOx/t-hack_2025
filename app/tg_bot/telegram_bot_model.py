import logging
from dotenv import load_dotenv
import os
import httpx
from telegram import Bot
from telegram.error import TelegramError

from app.tg_bot.message_generator import MessageGenerator

load_dotenv()
n8n_url = os.getenv('N8N_URL')

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
    
    async def send_msg_on_n8n(self, chat_id: int, msg: str):
        payload = {
        "userId": chat_id,
        "action": "sendMessage",
        "chatInput": msg
        }
        logger.info(f"N8N Отправлено сообщение: {msg}")
        async with httpx.AsyncClient() as client:
            try:
                await self.bot.send_message(
                        chat_id=chat_id,
                        text=f"⏳ Обрабатываем ваше сообщение..."
                    )
                response = await client.post(
                    n8n_url,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=30.0
                )
                response_data = response.json() if response.content else None
                response_data = {"name":"Работа","color":"#3498db","description":"Записи о работе и профессиональной деятельности"}
                response.status_code = 200
                match response.status_code:
                    case 200:
                        message_data = MessageGenerator(response_data).create_task()
                        await self.bot.send_message(
                            chat_id=chat_id,
                            text=message_data['text'],
                            parse_mode=message_data['parse_mode']
                        )
                        logger.info(
                            f"Успешный запрос к N8N | ChatID: {chat_id} | "
                            f"Status: {response.status_code} | Response: {response.text}"
                        )
                    case 422:
                        await self.bot.send_message(
                            chat_id=chat_id,
                            text="Я тебя не совсем понял. Пожалуйста, уточни детали твоего запроса."
                        )
                        # try:
                        #     clarification = await self.wait_for_clarification(chat_id, timeout=300)
                        #     if clarification:
                        #         return await self.send_msg_on_n8n(chat_id, f'{msg} {clarification}', expecting_clarification=True)
                        # except httpx.TimeoutException:
                        #     await self.bot.send_message(
                        #         chat_id=chat_id,
                        #         text="Время для уточнения истекло. Попробуйте снова."
                        #     )
                    case _:
                        error_message = f"HTTP Error {response.status_code}"
                        logger.error(
                            f"Ошибка запроса к N8N | ChatID: {chat_id} | \n"
                            f"Status: {response.status_code} | Response: {response.text}\n",
                            exc_info=True
                        )
                logger.info(f"N8N Status Code: {response.status_code}\nResponse: {response.text}")
            except httpx.TimeoutException:
                logger.info("N8N Request timed out")
                await self.bot.send_message(
                        chat_id=chat_id,
                        text=f"Превышено время ожидания сообщения",
                    )
            except Exception as e:
                logger.info(f"N8N An error occurred: {e}")
                await self.bot.send_message(
                    chat_id=chat_id,
                    text="Неизвестная ошибка, повторите позже..."
                )
            except TelegramError as e:
                logger.error(f"Ошибка отправки кода в Telegram: {e}")
                return False
            
telegram_bot = TelegramBot()