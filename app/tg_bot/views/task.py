from datetime import datetime
import logging
logger = logging.getLogger(__name__)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class TaskView:
    def __init__(self, data: dict, page: int = 0, per_page: int = 5):
        self.data = data
        self.page = page
        self.per_page = per_page
        self.parse_mode = 'HTML'
        self.total_tasks = len(data) if type(data) == list else 1
        self.total_pages = (self.total_tasks + per_page - 1) // per_page

    def _format_datetime(self, dt_str: str) -> str:
        """Форматирует строку с датой в читаемый вид"""
        try:
            dt = datetime.fromisoformat(dt_str.replace('+00:00', ''))
            return dt.strftime('%d.%m.%Y %H:%M')
        except (ValueError, AttributeError):
            return "не указано"

    def tasks_view(self) -> dict:
        tasks = self.data
        start = self.page * self.per_page
        end = start + self.per_page
        logger.info(f'{type(tasks)}')
        if not tasks:
            return {
                'text': "📭 <b>Задачи не найдены</b>",
                'parse_mode': self.parse_mode,
                'reply_markup': None
            }
        # if type(tasks is not list):
        #     return {
        #         'text': f"Ошибка: Неверный формат",
        #         'parse_mode': self.parse_mode,
        #         'reply_markup': None
        #     }
        page_tasks = tasks[start:end]
        message = [f"📋 <b>Задачи (стр. {self.page + 1}/{self.total_pages}):</b>\n"]
        
        for i, task in enumerate(page_tasks, start + 1):
            task_info = [
                f"{i}. 🎯 <b>{task.get('name', 'Без названия')}</b>",
                f"   📂 Категория: {task.get('category_name', 'Без категории')}",
                f"   🕘 Время: {self._format_datetime(task.get('start_time'))} - {self._format_datetime(task.get('deadline'))}",
                f"   📝 <i>{task.get('description', '')}</i>",
                ""
            ]
            message.extend(task_info)

        keyboard = []
        if self.total_pages > 1:
            nav_buttons = []
            if self.page > 0:
                nav_buttons.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"task_page_{self.page-1}"))
            if self.page < self.total_pages - 1:
                nav_buttons.append(InlineKeyboardButton("Вперед ➡️", callback_data=f"task_page_{self.page+1}"))
            keyboard.append(nav_buttons)
        
        keyboard.append([InlineKeyboardButton("❌ Закрыть", callback_data="close_tasks")])
        reply_markup = InlineKeyboardMarkup(keyboard) if keyboard else None

        return {
            'text': '\n'.join(message),
            'parse_mode': self.parse_mode,
            'reply_markup': reply_markup
        }