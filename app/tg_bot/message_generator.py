from telegram.constants import ParseMode

class MessageGenerator():
    def __init__(self, json_data: dict):
        self.data = json_data
        self.parse_mode = ParseMode.HTML  
        
    def _escape_html(self, text: str) -> str:
        """Экранирует спецсимволы для HTML"""
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def _format_time(self, time_str):
        if not time_str:
            return None
        return time_str.split('+')[0] if '+' in time_str else time_str

    def _get_color_type(self, hex_code: str) -> str:
        if not hex_code or len(hex_code) != 7 or not hex_code.startswith('#'):
            return "неизвестный цвет"
        
        try:
            r = int(hex_code[1:3], 16)
            g = int(hex_code[3:5], 16)
            b = int(hex_code[5:7], 16)
        except ValueError:
            return "некорректный цвет"

        r_pct = r / 2.55
        g_pct = g / 2.55
        b_pct = b / 2.55

        max_val = max(r, g, b)
        min_val = min(r, g, b)
        delta = max_val - min_val

        if delta < 10:
            if max_val < 30:
                return "черный"
            elif max_val > 230:
                return "белый"
            return "серый"

        hue = 0
        if delta != 0:
            if max_val == r:
                hue = (60 * ((g - b) / delta)) % 360
            elif max_val == g:
                hue = (60 * ((b - r) / delta) + 120) % 360
            else:
                hue = (60 * ((r - g) / delta) + 240) % 360

        if hue < 15 or hue >= 345:
            return "красный"
        elif 15 <= hue < 45:
            return "оранжевый"
        elif 45 <= hue < 75:
            return "желтый"
        elif 75 <= hue < 105:
            return "желто-зеленый"
        elif 105 <= hue < 135:
            return "зеленый"
        elif 135 <= hue < 165:
            return "зелено-бирюзовый"
        elif 165 <= hue < 195:
            return "бирюзовый"
        elif 195 <= hue < 225:
            return "голубой"
        elif 225 <= hue < 255:
            return "синий"
        elif 255 <= hue < 285:
            return "фиолетовый"
        elif 285 <= hue < 315:
            return "пурпурный"
        elif 315 <= hue < 345:
            return "розовый"
        return "смешанный цвет"

    def generate_answer(self):
        type = self.data.get('type')
        match type:
            case "task":
                return self.create_task()
            case "category":
                return self.create_category()

    def create_task(self) -> dict:
        task_name = self._escape_html(self.data.get('name', 'Без названия'))
        description = self._escape_html(self.data.get('description', ''))
        start_time = self.data.get('start_time')
        deadline = self.data.get('deadline')
        category = self.data.get('category_name')
        message_parts = [
            f"🎯 <b>Задача «{task_name}» успешно создана!\n</b>"
        ]
        if category:
            message_parts.append(f"\n✏️ <b>Категория:</b> <i>{category}</i>\n")
        if description:
            message_parts.append(f"\n📄 <b>Описание:</b>\n<i>{description}</i>\n")

        time_display = []
        if start_time:
            formatted_start = self._format_time(start_time)
            time_display.append(f"🟢 <b>Начало:</b> <code>{formatted_start}</code>\n")
        if deadline:
            formatted_deadline = self._format_time(deadline)
            if time_display:
                time_display.append(f"🔴 <b>Конец:</b> <code>{formatted_deadline}</code>\n")
            else:
                time_display.append(f"\n🔴 <b>Дедлайн:</b> <code>{formatted_deadline}</code>\n")
            
        if len(time_display) == 2:
            message_parts.append("\n⏳ <b>Временные метки:\n</b>")
        message_parts.extend(time_display)

        return {
            'text': ''.join(message_parts),
            'parse_mode': self.parse_mode
        }
    
    def create_category(self) -> str:
        color = self.data.get('color', '')
        cat_name = self.data.get('name')
        description = self.data.get('description')
        message_parts = [
            f"🎯 <b>Категория «{cat_name}» успешно создана!</b>\n"
        ]
        if description:
            message_parts.append(f"\n📄 <b>Описание:</b>\n<i>{description}</i>\n")
        if color:
            message_parts.append(f"\n🎨 <b>Цвет: {self._get_color_type(color)}</b>\n")

        return {
            'text': ''.join(message_parts),
            'parse_mode': self.parse_mode
        }
    def tasks_view(self) -> str:
        pass