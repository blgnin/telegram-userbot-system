import os
from dotenv import load_dotenv

print("🔧 Проверка конфигурации...")
print()

# Загружаем переменные окружения
load_dotenv()

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

print()
print("📋 Результат:")
if all([bot1_token, bot2_token, openai_key, chat_id]):
    print("🎉 Все настройки корректны! Можно запускать ботов.")
else:
    print("⚠️  Некоторые настройки отсутствуют.") 