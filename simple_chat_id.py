import asyncio
from telegram import Bot

# Вставьте сюда токен вашего первого бота
BOT_TOKEN = "8256494386:AAG3DlyV4nBAfxUrW1NIwXaF_04vYT19SU0"

async def get_chat_id():
    """Получает ID чата"""
    try:
        bot = Bot(token=BOT_TOKEN)
        
        # Получаем обновления
        updates = await bot.get_updates()
        
        if updates:
            print("📱 Найденные чаты:")
            for update in updates:
                if update.message:
                    chat_id = update.message.chat.id
                    chat_title = update.message.chat.title or "Личный чат"
                    user_name = update.message.from_user.first_name
                    
                    print(f"   Название: {chat_title}")
                    print(f"   ID чата: {chat_id}")
                    print(f"   Пользователь: {user_name}")
                    print(f"   Сообщение: {update.message.text}")
                    print()
                    print(f"✅ Добавьте этот ID в файл .env:")
                    print(f"   CHAT_ID={chat_id}")
                    print()
        else:
            print("❌ Сообщений не найдено.")
            print("💡 Отправьте любое сообщение боту и запустите скрипт снова.")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print("💡 Проверьте правильность токена бота")

if __name__ == "__main__":
    print("🔧 Инструкция:")
    print("1. Откройте файл simple_chat_id.py")
    print("2. Замените 'ВСТАВЬТЕ_СЮДА_ТОКЕН_ПЕРВОГО_БОТА' на реальный токен")
    print("3. Отправьте сообщение боту в Telegram")
    print("4. Запустите этот скрипт снова")
    print()
    
    if BOT_TOKEN == "ВСТАВЬТЕ_СЮДА_ТОКЕН_ПЕРВОГО_БОТА":
        print("⚠️  Сначала замените токен в файле!")
    else:
        asyncio.run(get_chat_id()) 