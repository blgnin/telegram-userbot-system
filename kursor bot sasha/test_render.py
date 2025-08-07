#!/usr/bin/env python3
"""
Минимальный тест для Render.com
"""
import sys
import os

print("=" * 50)
print("🔍 ТЕСТ RENDER.COM ЗАПУЩЕН!")
print("=" * 50)

print(f"Python версия: {sys.version}")
print(f"Рабочая директория: {os.getcwd()}")
print(f"Python путь: {sys.executable}")

# Проверяем переменные окружения
required_vars = ['BOT1_TOKEN', 'BOT2_TOKEN', 'BOT3_TOKEN', 'OPENAI_API_KEY', 'CHAT_ID', 'RENDER']

print("\n🔍 Проверка переменных окружения:")
for var in required_vars:
    value = os.environ.get(var)
    if value:
        print(f"✅ {var}: {'***' + value[-4:] if len(value) > 4 else 'НАЙДЕН'}")
    else:
        print(f"❌ {var}: НЕ НАЙДЕН")

print("\n📁 Содержимое текущей директории:")
try:
    files = os.listdir('.')
    for f in sorted(files):
        print(f"  - {f}")
except Exception as e:
    print(f"Ошибка чтения директории: {e}")

print("\n🔍 Ищем main_render.py:")
for root, dirs, files in os.walk('.'):
    for file in files:
        if file == 'main_render.py':
            full_path = os.path.join(root, file)
            print(f"✅ Найден: {full_path}")

print("\n✅ ТЕСТ ЗАВЕРШЕН УСПЕШНО!")
print("=" * 50)
