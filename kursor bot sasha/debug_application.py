import asyncio
import logging
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import BOT1_TOKEN, CHAT_ID, BOT1_NAME
from ai_handler import AIHandler

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class SimpleBot:
    def __init__(self):
        self.ai_handler = AIHandler()
        
    async def start_command(self, update, context):
        """Обработчик команды /start"""
        try:
            await update.message.reply_text("🚀 Бот запущен! Отправьте любое сообщение для начала разговора о GOMINIAPP.")
            logger.info("✅ Команда /start получена")
        except Exception as e:
            logger.error(f"❌ Ошибка в start_command: {e}")
    
    async def handle_message(self, update, context):
        """Обработчик сообщений"""
        try:
            message_text = update.message.text
            logger.info(f"📝 Получено сообщение: {message_text}")
            
            # Генерируем ответ через AI
            response = await self.ai_handler.generate_response(
                message_text, 
                BOT1_NAME,
                f"Пользователь написал: {message_text}"
            )
            
            await update.message.reply_text(f"🤖 {BOT1_NAME}: {response}")
            logger.info("✅ Ответ отправлен")
            
        except Exception as e:
            logger.error(f"❌ Ошибка в handle_message: {e}")
            await update.message.reply_text("❌ Произошла ошибка при обработке сообщения")

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

async def test_application():
    """Тестирует Application без run_polling"""
    try:
        print("🔧 Тестируем Application...")
        
        # Создаем бота
        bot = SimpleBot()
        
        # Создаем приложение
        app = Application.builder().token(BOT1_TOKEN).build()
        
        # Добавляем обработчики
        app.add_handler(CommandHandler("start", bot.start_command))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
        
        print("✅ Application создан")
        print("✅ Обработчики добавлены")
        
        # Проверяем методы Application
        print("🔍 Проверяем методы Application:")
        print(f"   - app.bot: {app.bot}")
        print(f"   - app.updater: {app.updater}")
        
        # Пробуем запустить без run_polling
        print("🔄 Запускаем updater.start_polling()...")
        await app.updater.start_polling()
        
        print("✅ Updater запущен успешно!")
        
        # Ждем немного
        await asyncio.sleep(5)
        
        # Останавливаем
        await app.updater.stop()
        print("✅ Updater остановлен")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Главная функция"""
    print("🚀 Отладка Application...")
    print()
    
    # Проверяем event loop
    loop = check_event_loop()
    print()
    
    try:
        # Создаем новый event loop
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        
        # Запускаем тест
        new_loop.run_until_complete(test_application())
        
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            new_loop.close()
        except:
            pass

if __name__ == "__main__":
    main() 