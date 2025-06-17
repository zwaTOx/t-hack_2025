class MessageGenerator():
    def __init__(self, json: dict):
        self.data = json

    def create_task(self) -> str:
        message = "🎯 <b>Задача успешно создана!</b>\n\n"
        message += f"📌 <b>Название:</b> {self.data.get('name', 'Без названия')}\n"
        if 'color' in self.data:
            message += f"🎨 <b>Цвет задачи:</b> {self.data['color']}\n"
        if 'description' in self.data and self.data['description']:
            message += f"\n📋 <b>Описание:</b>\n{self.data['description']}\n"
        if 'deadline' in self.data and self.data['deadline']:
            message += f"\n🕙 <b>Время:</b>\n{self.data['deadline']}\n"
        return message
    
    def create_category(self):
        pass