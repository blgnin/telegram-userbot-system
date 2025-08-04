import os
from dotenv import load_dotenv

# Загружаем переменные из файла shlyapa1.env
load_dotenv('shlyapa1.env')

# Проверяем загрузку переменных
print("🔍 Проверка переменных окружения:")
print(f"BOT1_TOKEN: {os.getenv('BOT1_TOKEN')}")
print(f"BOT2_TOKEN: {os.getenv('BOT2_TOKEN')}")
print(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY')}")
print(f"CHAT_ID: {os.getenv('CHAT_ID')}")

# Проверяем, что файл существует
import os.path
print(f"\n📁 Файл shlyapa1.env существует: {os.path.exists('shlyapa1.env')}")

if os.path.exists('shlyapa1.env'):
    with open('shlyapa1.env', 'r', encoding='utf-8') as f:
        content = f.read()
        print(f"\n📄 Содержимое файла shlyapa1.env:")
        print(content) 