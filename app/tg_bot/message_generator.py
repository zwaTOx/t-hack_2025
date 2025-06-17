from telegram.constants import ParseMode

class MessageGenerator():
    def __init__(self, json_data: dict):
        self.data = json_data
        self.parse_mode = ParseMode.HTML  
        
    def _escape_html(self, text: str) -> str:
        """Экранирует спецсимволы для HTML"""
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def get_color_type(self, hex_code: str) -> str:
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

    def create_task(self) -> dict:
        task_name = self._escape_html(self.data.get('name', 'Без названия'))
        color = self.data.get('color', '')
        description = self._escape_html(self.data.get('description', ''))
        deadline = self.data.get('deadline')

        if color:
            color_display = (
                f"\n\n🎨 <b>Цвет: {self.get_color_type(color)}</b>\n"
            )

        message_parts = [
            f"🎯 <b>Задача «{task_name}» успешно создана!</b>",
            color_display
        ]

        if description:
            message_parts.append(f"\n📄 <b>Описание:</b>\n<i>{description}</i>")

        if deadline:
            message_parts.append(f"\n\n⏰ <b>Срок выполнения:</b>\n<code>{deadline}</code>")

        return {
            'text': ''.join(message_parts),
            'parse_mode': self.parse_mode
        }
    
    def create_category(self) -> str:
        pass

    def tasks_view(self) -> str:
        pass