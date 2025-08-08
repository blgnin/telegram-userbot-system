#!/usr/bin/env python3
"""
Главный файл для Railway.app
Запускает Telegram юзер-ботов с веб-сервером
"""
import asyncio

# Импортируем и запускаем основной модуль
if __name__ == "__main__":
    from main_render import main
    
    print("🚀 Запуск Telegram Userbot System на Railway.app")
    asyncio.run(main())
