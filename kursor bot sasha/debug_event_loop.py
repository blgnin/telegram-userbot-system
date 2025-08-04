import asyncio
import logging
from telegram import Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import BOT1_TOKEN, CHAT_ID, BOT1_NAME
from ai_handler import AIHandler

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def check_event_loop():
    """Проверяет состояние event loop"""
    try:
        loop = asyncio.get_event_loop()
        print(f"✅ Event loop найден: {loop}")
        print(f"   Запущен: {loop.is_running()}")
        print(f"   Закрыт: {loop.is_closed()}")
        return loop
    except RuntimeError as e:
        print(f"❌ Event loop не найден: {e}")
        return None

async def test_bot_setup():
    """Тестирует настройку бота"""
    try:
        print("🔧 Тестируем настройку бота...")
        
        # Создаем приложение
        app = Application.builder().token(BOT1_TOKEN).build()
        print("✅ Application создан")
        
        # Добавляем простой обработчик
        async def test_handler(update, context):
            await update.message.reply_text("Тест")
        
        app.add_handler(CommandHandler("test", test_handler))
        print("✅ Обработчик добавлен")
        
        print("✅ Настройка бота прошла успешно")
        return app
        
    except Exception as e:
        print(f"❌ Ошибка настройки бота: {e}")
        return None

async def main():
    """Главная функция"""
    print("🚀 Отладка event loop...")
    print()
    
    # Проверяем event loop
    loop = check_event_loop()
    print()
    
    # Тестируем настройку бота
    app = await test_bot_setup()
    print()
    
    if app:
        print("✅ Все тесты прошли успешно!")
    else:
        print("❌ Тесты не прошли")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}") 