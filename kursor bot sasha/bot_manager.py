import asyncio
import logging
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import BOT1_TOKEN, BOT2_TOKEN, CHAT_ID, BOT1_NAME, BOT2_NAME
from ai_handler import AIHandler

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class BotManager:
    def __init__(self):
        try:
            self.bot1 = Bot(token=BOT1_TOKEN)
            self.bot2 = Bot(token=BOT2_TOKEN)
            self.ai_handler = AIHandler()
            self.conversation_active = False
            self.current_speaker = None
            logger.info(f"✅ Боты инициализированы: {BOT1_NAME}, {BOT2_NAME}")
        except Exception as e:
            logger.error(f"❌ Ошибка инициализации ботов: {e}")
            raise
        
    async def start_conversation(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Начинает разговор между ботами"""
        try:
            if self.conversation_active:
                await update.message.reply_text("🔄 Разговор уже идет!")
                return
            
            logger.info("🎬 Начинаем разговор о GOMINIAPP...")
            self.conversation_active = True
            self.current_speaker = BOT1_NAME
            self.ai_handler.clear_history()
            
            # Отправляем первое сообщение от первого бота (водителя)
            initial_message = await self.ai_handler.generate_response(
                "Привет! Я водитель в GOMINIAPP. Недавно попробовал это приложение для совместных поездок. Очень удобно - никаких комиссий, гибкие цены, и можно зарабатывать токены GO. Что думаешь о таких сервисах?", 
                BOT1_NAME
            )
            
            await update.message.reply_text(initial_message)
            await update.message.reply_text("🎉 Разговор о GOMINIAPP начался! Отправьте любое сообщение для продолжения.")
            logger.info("✅ Разговор успешно начат")
            
        except Exception as e:
            logger.error(f"❌ Ошибка при начале разговора: {e}")
            await update.message.reply_text("❌ Ошибка при начале разговора")
    
    async def stop_conversation(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Останавливает разговор между ботами"""
        try:
            self.conversation_active = False
            await update.message.reply_text("⏹️ Разговор остановлен.")
            logger.info("🛑 Разговор остановлен пользователем")
        except Exception as e:
            logger.error(f"❌ Ошибка при остановке разговора: {e}")
    

    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обрабатывает сообщения от пользователя"""
        try:
            message_text = update.message.text
            logger.info(f"👤 Пользователь написал: {message_text}")
            
            # Если разговор не активен, начинаем его
            if not self.conversation_active:
                self.conversation_active = True
                self.current_speaker = BOT1_NAME
                self.ai_handler.clear_history()
                await update.message.reply_text("🎉 Разговор о GOMINIAPP начался! Отправьте любое сообщение для продолжения.")
            
            # Определяем какой бот должен ответить
            if self.current_speaker == BOT1_NAME:
                bot_name = BOT2_NAME
                self.current_speaker = BOT2_NAME
            else:
                bot_name = BOT1_NAME
                self.current_speaker = BOT1_NAME
            
            # Генерируем ответ на сообщение пользователя
            response = await self.ai_handler.generate_response(message_text, bot_name)
            
            # Отправляем ответ пользователю
            await update.message.reply_text(response)
            
            logger.info(f"💬 {bot_name} ответил на сообщение пользователя")
            
        except Exception as e:
            logger.error(f"❌ Ошибка при обработке сообщения пользователя: {e}")
            await update.message.reply_text("Привет! Давайте поговорим о GOMINIAPP - это отличное приложение для совместных поездок. Что тебя интересует?")
    
    async def setup_bot1(self):
        """Настраивает первого бота"""
        try:
            app = Application.builder().token(BOT1_TOKEN).build()
            
            # Добавляем обработчики
            app.add_handler(CommandHandler("start", self.start_conversation))
            app.add_handler(CommandHandler("stop", self.stop_conversation))
            app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
            
            logger.info(f"✅ {BOT1_NAME} настроен")
            return app
            
        except Exception as e:
            logger.error(f"❌ Ошибка настройки {BOT1_NAME}: {e}")
            raise
    
    async def setup_bot2(self):
        """Настраивает второго бота"""
        try:
            app = Application.builder().token(BOT2_TOKEN).build()
            
            # Добавляем обработчики
            app.add_handler(CommandHandler("start", self.start_conversation))
            app.add_handler(CommandHandler("stop", self.stop_conversation))
            app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
            
            logger.info(f"✅ {BOT2_NAME} настроен")
            return app
            
        except Exception as e:
            logger.error(f"❌ Ошибка настройки {BOT2_NAME}: {e}")
            raise 