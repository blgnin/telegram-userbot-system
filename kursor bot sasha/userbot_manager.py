import asyncio
import logging
from telethon import TelegramClient, events
from telethon.tl.types import PeerUser, PeerChat
from config import BOT1_TOKEN, BOT2_TOKEN, CHAT_ID, BOT1_NAME, BOT2_NAME
from ai_handler import AIHandler

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class UserBotManager:
    def __init__(self):
        try:
            # Создаем клиенты для юзер-ботов
            self.client1 = TelegramClient('session1', api_id=2040, api_hash='b18441a1ff607e10a989891a5462e627')
            self.client2 = TelegramClient('session2', api_id=2040, api_hash='b18441a1ff607e10a989891a5462e627')
            
            self.ai_handler = AIHandler()
            self.conversation_active = False
            self.current_speaker = None
            self.last_responses = {}  # Словарь для отслеживания последних ответов
            self.response_times = {}  # Словарь для отслеживания времени ответов
            logger.info(f"✅ Юзер-боты инициализированы: {BOT1_NAME}, {BOT2_NAME}")
        except Exception as e:
            logger.error(f"❌ Ошибка инициализации юзер-ботов: {e}")
            raise
    
    async def start_conversation(self, event):
        """Начинает разговор между юзер-ботами"""
        try:
            if self.conversation_active:
                await event.reply("🔄 Система уже активна!")
                return
            
            logger.info("🎬 Активируем систему юзер-ботов...")
            self.conversation_active = True
            self.current_speaker = BOT1_NAME
            self.ai_handler.clear_history()
            
            await event.reply("🎉 Система юзер-ботов активирована! Боты будут отвечать на сообщения пользователей и друг друга. Используйте функцию 'Reply' (ответить) в Telegram на любое сообщение.")
            logger.info("✅ Система успешно активирована")
            
        except Exception as e:
            logger.error(f"❌ Ошибка при активации системы: {e}")
            await event.reply("❌ Ошибка при активации системы")
    
    async def stop_conversation(self, event):
        """Останавливает разговор между юзер-ботами"""
        try:
            self.conversation_active = False
            await event.reply("⏹️ Разговор остановлен.")
            logger.info("🛑 Разговор остановлен пользователем")
        except Exception as e:
            logger.error(f"❌ Ошибка при остановке разговора: {e}")
    
    async def handle_message(self, event):
        """Обрабатывает сообщения от пользователя"""
        try:
            import time
            from datetime import datetime, timedelta
            
            message_text = event.message.text
            sender_id = event.sender_id
            
            # Проверяем, является ли это ответом на сообщение (Reply)
            is_reply = event.message.reply_to is not None
            
            if is_reply:
                logger.info(f"👤 Получен ответ на сообщение: {message_text}")
                logger.info(f"🔍 ID отправителя: {sender_id}")
                
                # Получаем ID ботов
                me1 = await self.client1.get_me()
                me2 = await self.client2.get_me()
                logger.info(f"🔍 ID ботов: {me1.id}, {me2.id}")
                
                # Проверяем, что система активна
                if not self.conversation_active:
                    logger.info(f"📝 Система не активна, игнорируем")
                    return
                
                # Проверяем, что бот отвечает на своё сообщение
                try:
                    replied_message = await event.get_reply_message()
                    if not replied_message:
                        logger.info(f"🚫 Нет сообщения для ответа, игнорируем")
                        return
                    
                                         # Проверяем, что бот отвечает на сообщение другого бота или пользователя
                    logger.info(f"🔍 Проверяем отправителя: replied_message.sender_id={replied_message.sender_id}, sender_id={sender_id}")
                    if replied_message.sender_id != sender_id:
                        logger.info(f"✅ Бот отвечает на сообщение другого бота или пользователя, продолжаем")
                    else:
                        logger.info(f"🚫 Бот отвечает на своё сообщение, игнорируем")
                        return
                    
                    # Определяем какой бот должен ответить (тот, кто получил Reply)
                    if replied_message.sender_id == me1.id:  # Если Reply на сообщение первого бота
                        bot_name = BOT1_NAME
                    elif replied_message.sender_id == me2.id:  # Если Reply на сообщение второго бота
                        bot_name = BOT2_NAME
                    else:
                        logger.info(f"🚫 Неизвестный получатель Reply, игнорируем")
                        return
                        
                    # Проверяем, что боты не отвечают на системные сообщения
                    if replied_message.text:
                        system_messages = [
                            "🔄 Система уже активна!",
                            "🎉 Система юзер-ботов активирована! Боты будут отвечать на сообщения пользователей и друг друга. Используйте функцию 'Reply' (ответить) в Telegram на любое сообщение.",
                            "⏹️ Разговор остановлен."
                        ]
                        # Убираем проверку системных сообщений, чтобы боты могли отвечать друг другу
                        # if replied_message.text in system_messages:
                        #     logger.info(f"🚫 Бот отвечает на системное сообщение, игнорируем")
                        #     return
                        
                except Exception as e:
                    logger.info(f"⚠️ Не удалось проверить отправителя: {e}")
                    return
                
                # Логика определения бота уже определена выше
                
                # Проверяем, не повторяется ли ответ в течение часа
                current_time = datetime.now()
                if bot_name in self.response_times:
                    time_diff = current_time - self.response_times[bot_name]
                    if time_diff < timedelta(seconds=30):  # Уменьшаем до 30 секунд
                        logger.info(f"⏰ {bot_name} отвечал менее 30 секунд назад, пропускаем")
                        return
                
                # Добавляем задержку 10 секунд перед ответом
                logger.info(f"⏰ {bot_name} ждет 10 секунд перед ответом...")
                await asyncio.sleep(10)
                
                # Генерируем ответ на сообщение пользователя
                response = await self.ai_handler.generate_response(message_text, bot_name)
                
                # Проверяем, не повторяется ли ответ
                if bot_name in self.last_responses and response == self.last_responses[bot_name]:
                    logger.info(f"🔄 {bot_name} пытается повторить ответ, генерируем новый")
                    response = await self.ai_handler.generate_response(message_text + " (новый ответ)", bot_name)
                
                # Сохраняем ответ и время
                self.last_responses[bot_name] = response
                self.response_times[bot_name] = current_time
                
                # Отправляем ответ пользователю
                await event.reply(response)
                
                logger.info(f"💬 {bot_name} ответил на сообщение пользователя")
            else:
                # Если это не Reply, просто логируем сообщение
                logger.info(f"📝 Получено обычное сообщение: {message_text}")
            
        except Exception as e:
            logger.error(f"❌ Ошибка при обработке сообщения пользователя: {e}")
            await event.reply("Привет! Давайте поговорим о GOMINIAPP - это отличное приложение для совместных поездок. Что тебя интересует?")
    
    async def setup_userbot1(self):
        """Настраивает первого юзер-бота"""
        try:
            # Проверяем, что номер телефона загружен
            if not BOT1_TOKEN or BOT1_TOKEN == 'your_phone1_here':
                raise ValueError("Номер телефона для первого юзер-бота не найден. Проверьте файл shlyapa1.env")
            
            # Подключаемся к Telegram
            await self.client1.start(phone=BOT1_TOKEN)
            
            # Регистрируем обработчики событий
            # Maria НЕ реагирует на /start и /stop
            # Maria отвечает ТОЛЬКО на Reply
            @self.client1.on(events.NewMessage())
            async def message_handler(event):
                # Проверяем, что это Reply
                if event.message.reply_to is not None:
                    await self.handle_message(event)
            
            logger.info(f"✅ {BOT1_NAME} настроен")
            return self.client1
            
        except Exception as e:
            logger.error(f"❌ Ошибка настройки {BOT1_NAME}: {e}")
            raise
    
    async def setup_userbot2(self):
        """Настраивает второго юзер-бота"""
        try:
            # Проверяем, что номер телефона загружен
            if not BOT2_TOKEN or BOT2_TOKEN == 'your_phone2_here':
                raise ValueError("Номер телефона для второго юзер-бота не найден. Проверьте файл shlyapa1.env")
            
            # Подключаемся к Telegram
            await self.client2.start(phone=BOT2_TOKEN)
            
            # Регистрируем обработчики событий
            @self.client2.on(events.NewMessage(pattern='/start'))
            async def start_handler(event):
                await self.start_conversation(event)
            
            @self.client2.on(events.NewMessage(pattern='/stop'))
            async def stop_handler(event):
                await self.stop_conversation(event)
            
            @self.client2.on(events.NewMessage())
            async def message_handler(event):
                # Проверяем, что это Reply
                if event.message.reply_to is not None:
                    await self.handle_message(event)
            
            logger.info(f"✅ {BOT2_NAME} настроен")
            return self.client2
            
        except Exception as e:
            logger.error(f"❌ Ошибка настройки {BOT2_NAME}: {e}")
            raise 