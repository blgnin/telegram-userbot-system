import asyncio
import logging
from bot_manager import BotManager
from telegram import Update

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def run_bot(app, bot_name):
    """Запускает одного бота"""
    try:
        logger.info(f"🔄 Запуск {bot_name}...")
        await app.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        logger.error(f"❌ Ошибка {bot_name}: {e}")

async def main():
    """Главная функция для запуска ботов"""
    try:
        logger.info("🚀 Запуск системы общения ботов...")
        
        # Создаем менеджер ботов
        bot_manager = BotManager()
        
        # Настраиваем приложения для каждого бота
        logger.info("📱 Настройка ботов...")
        app1 = await bot_manager.setup_bot1()
        app2 = await bot_manager.setup_bot2()
        
        logger.info("✅ Боты настроены успешно!")
        logger.info("💬 Используйте команду /start в чате для начала разговора")
        logger.info("🛑 Используйте команду /stop для остановки разговора")
        logger.info("📝 Любое текстовое сообщение - вмешаться в разговор")
        
        # Запускаем ботов одновременно
        logger.info("🔄 Запуск ботов...")
        
        # Запускаем оба бота одновременно
        await asyncio.gather(
            run_bot(app1, "Алексей (водитель)"),
            run_bot(app2, "Мария (пассажир)")
        )
        
    except KeyboardInterrupt:
        logger.info("⏹️  Получен сигнал остановки. Завершение работы...")
    except Exception as e:
        logger.error(f"❌ Ошибка при запуске: {e}")
        logger.error("🔧 Проверьте настройки в файле .env")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️  Система остановлена пользователем")
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}") 