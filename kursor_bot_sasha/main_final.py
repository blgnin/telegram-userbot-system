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

class SimpleBot:
    def __init__(self):
        self.ai_handler = AIHandler()
        self.conversation_active = False
        
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

def main():
    """Главная функция"""
    print("🚀 Запуск простого бота...")
    print("💬 Отправьте /start боту в Telegram")
    print("🛑 Нажмите Ctrl+C для остановки")
    print()
    
    try:
        # Создаем новый event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def run_bot():
            """Запуск бота"""
            try:
                logger.info("🚀 Запуск простого бота...")
                
                # Создаем бота
                bot = SimpleBot()
                
                # Создаем приложение
                app = Application.builder().token(BOT1_TOKEN).build()
                
                # Добавляем обработчики
                app.add_handler(CommandHandler("start", bot.start_command))
                app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
                
                logger.info("✅ Бот настроен!")
                logger.info("💬 Отправьте /start боту в Telegram")
                
                # Запускаем бота
                await app.run_polling()
                
            except Exception as e:
                logger.error(f"❌ Ошибка: {e}")
        
        # Запускаем бота
        loop.run_until_complete(run_bot())
        
    except KeyboardInterrupt:
        print("\n⏹️  Бот остановлен")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        # Закрываем loop
        try:
            loop.close()
        except:
            pass

if __name__ == "__main__":
    main() 