import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

print("🔧 Проверка конфигурации:")
print()

# Проверяем токены ботов
bot1_token = os.getenv('BOT1_TOKEN')
bot2_token = os.getenv('BOT2_TOKEN')
openai_key = os.getenv('OPENAI_API_KEY')
chat_id = os.getenv('CHAT_ID')

print("📱 Токены ботов:")
if bot1_token and bot1_token != 'your_bot1_token_here':
    print("✅ BOT1_TOKEN: настроен")
else:
    print("❌ BOT1_TOKEN: не настроен")

if bot2_token and bot2_token != 'your_bot2_token_here':
    print("✅ BOT2_TOKEN: настроен")
else:
    print("❌ BOT2_TOKEN: не настроен")

print()
print("🧠 OpenAI API:")
if openai_key and openai_key != 'your_openai_api_key_here':
    print("✅ OPENAI_API_KEY: настроен")
else:
    print("❌ OPENAI_API_KEY: не настроен")

print()
print("💬 ID чата:")
if chat_id and chat_id != 'your_chat_id_here':
    print(f"✅ CHAT_ID: {chat_id}")
else:
    print("❌ CHAT_ID: не настроен")
    print("💡 Запустите simple_chat_id.py для получения ID")

print()
print("📋 Что нужно сделать:")
if not (bot1_token and bot1_token != 'your_bot1_token_here'):
    print("1. Добавьте токен первого бота в .env")
if not (bot2_token and bot2_token != 'your_bot2_token_here'):
    print("2. Добавьте токен второго бота в .env")
if not (openai_key and openai_key != 'your_openai_api_key_here'):
    print("3. Добавьте OpenAI API ключ в .env")
if not (chat_id and chat_id != 'your_chat_id_here'):
    print("4. Получите ID чата и добавьте в .env") 