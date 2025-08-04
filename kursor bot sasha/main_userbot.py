import asyncio
import logging
import tracemalloc
from userbot_manager import UserBotManager

# Включаем tracemalloc для отслеживания памяти
tracemalloc.start()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def main():
    """Главная функция для запуска юзер-ботов"""
    try:
        logger.info("🚀 Запуск системы юзер-ботов...")
        
        # Создаем менеджер юзер-ботов
        userbot_manager = UserBotManager()
        
        logger.info("📱 Настройка юзер-ботов...")
        
        # Настраиваем первого юзер-бота
        client1 = await userbot_manager.setup_userbot1()
        
        # Настраиваем второго юзер-бота
        client2 = await userbot_manager.setup_userbot2()
        
        logger.info("✅ Юзер-боты настроены успешно!")
        logger.info("💬 Используйте команду /start в чате для начала разговора")
        logger.info("🛑 Используйте команду /stop для остановки разговора")
        logger.info("📝 Любое текстовое сообщение - вмешаться в разговор")
        logger.info("🔄 Запуск юзер-ботов...")
        
        # Запускаем юзер-ботов
        await asyncio.gather(
            client1.run_until_disconnected(),
            client2.run_until_disconnected()
        )
        
    except KeyboardInterrupt:
        logger.info("🛑 Получен сигнал остановки")
    except Exception as e:
        logger.error(f"❌ Ошибка при запуске: {e}")
        logger.error("🔧 Проверьте настройки в файле .env")

if __name__ == "__main__":
    asyncio.run(main()) 