#!/usr/bin/env python3
"""
Главный файл для Railway.app
Запускает Telegram юзер-ботов с веб-сервером
"""
import sys
import os

# Добавляем путь к нашим модулям
sys.path.append(os.path.join(os.path.dirname(__file__), 'kursor bot sasha'))

# Импортируем и запускаем основной модуль
if __name__ == "__main__":
    from main_render import main
    import asyncio
    
    print("🚀 Запуск Telegram Userbot System на Railway.app")
    asyncio.run(main())
