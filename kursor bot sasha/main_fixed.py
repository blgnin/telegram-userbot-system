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

def main():
    """Главная функция для запуска ботов"""
    print("🚀 Запуск системы общения ботов...")
    print("💬 Используйте команду /start в чате для начала разговора")
    print("🛑 Используйте команду /stop для остановки разговора")
    print("📝 Любое текстовое сообщение - вмешаться в разговор")
    print("🛑 Нажмите Ctrl+C для остановки")
    print()
    
    try:
        # Создаем новый event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def run_bots():
            """Запуск ботов"""
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

                # Запускаем ботов последовательно
                logger.info("🔄 Запуск ботов последовательно...")
                
                # Сначала запускаем первого бота
                logger.info("🔄 Запуск первого бота (Алексей)...")
                await app1.run_polling(allowed_updates=Update.ALL_TYPES)
                
                # Если первый бот остановился, запускаем второго
                logger.info("🔄 Запуск второго бота (Мария)...")
                await app2.run_polling(allowed_updates=Update.ALL_TYPES)

            except KeyboardInterrupt:
                logger.info("⏹️  Получен сигнал остановки. Завершение работы...")
            except Exception as e:
                logger.error(f"❌ Ошибка при запуске: {e}")
                logger.error("🔧 Проверьте настройки в файле .env")
        
        # Запускаем ботов
        loop.run_until_complete(run_bots())
        
    except KeyboardInterrupt:
        print("\n⏹️  Система остановлена пользователем")
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
    finally:
        # Закрываем loop
        try:
            loop.close()
        except:
            pass
        # Останавливаем tracemalloc
        tracemalloc.stop()

if __name__ == "__main__":
    main() 