import asyncio
import logging
from telegram import Bot
from config import BOT1_TOKEN

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def get_chat_id():
    """Получает ID чата при получении сообщения"""
    bot = Bot(token=BOT1_TOKEN)
    
    # Получаем обновления
    updates = await bot.get_updates()
    
    if updates:
        for update in updates:
            if update.message:
                chat_id = update.message.chat.id
                chat_title = update.message.chat.title or "Личный чат"
                user_name = update.message.from_user.first_name
                
                print(f"📱 Найден чат:")
                print(f"   Название: {chat_title}")
                print(f"   ID чата: {chat_id}")
                print(f"   Пользователь: {user_name}")
                print(f"   Сообщение: {update.message.text}")
                print()
                print(f"✅ Добавьте этот ID в файл .env:")
                print(f"   CHAT_ID={chat_id}")
    else:
        print("❌ Сообщений не найдено.")
        print("💡 Отправьте любое сообщение боту и запустите скрипт снова.")

if __name__ == "__main__":
    asyncio.run(get_chat_id()) 