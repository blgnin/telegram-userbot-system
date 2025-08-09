import os
from dotenv import load_dotenv

# Загружаем переменные из файла shlyapa1.env
load_dotenv('shlyapa1.env')

# Номера телефонов для юзер-ботов (замените на реальные номера)
BOT1_TOKEN = os.getenv('BOT1_TOKEN', 'your_phone1_here')  # Теперь это номер телефона
BOT2_TOKEN = os.getenv('BOT2_TOKEN', 'your_phone2_here')  # Теперь это номер телефона
BOT3_TOKEN = os.getenv('BOT3_TOKEN', '+38268207785')  # Алевтина

# Отладочная информация
print(f"Загруженные номера телефонов:")
print(f"BOT1_TOKEN: {BOT1_TOKEN}")
print(f"BOT2_TOKEN: {BOT2_TOKEN}")
print(f"BOT3_TOKEN: {BOT3_TOKEN}")

# OpenAI API ключ
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your_openai_api_key_here')

# ID рабочего чата (где боты общаются)
CHAT_ID = os.getenv('CHAT_ID', 'your_chat_id_here')

# ID управляющего чата (где принимаем /start, /stop, /check)
CONTROL_CHAT_ID = os.getenv('CONTROL_CHAT_ID', CHAT_ID)

# Настройки AI
AI_MODEL = "gpt-3.5-turbo"
MAX_TOKENS = 200
TEMPERATURE = 0.8

# Имена ботов для тематики GOMINIAPP
BOT1_NAME = "Daniel"
BOT2_NAME = "Leonardo" 
BOT3_NAME = "Алевтина" 