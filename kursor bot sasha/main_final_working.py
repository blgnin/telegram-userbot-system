import asyncio
import logging
import tracemalloc
from bot_manager import BotManager
from telegram import Update

# Включаем tracemalloc для отслеживания памяти
tracemalloc.start()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def run_single_bot():
    """Запускает одного бота"""
    try:
        logger.info("🚀 Запуск системы общения ботов...")

        # Создаем менеджер ботов
        bot_manager = BotManager()

        # Настраиваем только первого бота
        logger.info("📱 Настройка бота...")
        app1 = await bot_manager.setup_bot1()

        logger.info("✅ Бот настроен успешно!")
        logger.info("💬 Используйте команду /start в чате для начала разговора")
        logger.info("🛑 Используйте команду /stop для остановки разговора")
        logger.info("📝 Любое текстовое сообщение - вмешаться в разговор")

        # Запускаем бота
        logger.info("🔄 Запуск бота Алексей (водитель)...")
        await app1.run_polling(allowed_updates=Update.ALL_TYPES)

    except KeyboardInterrupt:
        logger.info("⏹️  Получен сигнал остановки. Завершение работы...")
    except Exception as e:
        logger.error(f"❌ Ошибка при запуске: {e}")
        logger.error("🔧 Проверьте настройки в файле .env")

def main():
    """Главная функция"""
    print("🚀 Запуск системы общения ботов...")
    print("💬 Используйте команду /start в чате для начала разговора")
    print("🛑 Используйте команду /stop для остановки разговора")
    print("📝 Любое текстовое сообщение - вмешаться в разговор")
    print("🛑 Нажмите Ctrl+C для остановки")
    print()
    
    try:
        # Запускаем бота
        asyncio.run(run_single_bot())
        
    except KeyboardInterrupt:
        print("\n⏹️  Система остановлена пользователем")
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
    finally:
        # Останавливаем tracemalloc
        tracemalloc.stop()

if __name__ == "__main__":
    main() 