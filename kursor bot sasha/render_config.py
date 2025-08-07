"""
Конфигурация для Render.com
Загружает переменные окружения из системы (для продакшена)
"""
import os
from pathlib import Path

# Для Render.com используем системные переменные окружения
BOT1_TOKEN = os.environ.get('BOT1_TOKEN')
BOT2_TOKEN = os.environ.get('BOT2_TOKEN') 
BOT3_TOKEN = os.environ.get('BOT3_TOKEN')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
CHAT_ID = os.environ.get('CHAT_ID')

# Проверяем наличие всех необходимых переменных
required_vars = {
    'BOT1_TOKEN': BOT1_TOKEN,
    'BOT2_TOKEN': BOT2_TOKEN,
    'BOT3_TOKEN': BOT3_TOKEN,
    'OPENAI_API_KEY': OPENAI_API_KEY,
    'CHAT_ID': CHAT_ID
}

missing_vars = [name for name, value in required_vars.items() if not value]
if missing_vars:
    raise ValueError(f"Отсутствуют переменные окружения: {', '.join(missing_vars)}")

# Настройки AI
AI_MODEL = "gpt-3.5-turbo"
MAX_TOKENS = 200
TEMPERATURE = 0.8

# Имена ботов для тематики GOMINIAPP
BOT1_NAME = "Daniel"
BOT2_NAME = "Leonardo" 
BOT3_NAME = "Алевтина"

print("✅ Конфигурация Render.com загружена успешно")
print(f"🤖 Боты: {BOT1_NAME}, {BOT2_NAME}, {BOT3_NAME}")
print(f"💬 Chat ID: {CHAT_ID}")