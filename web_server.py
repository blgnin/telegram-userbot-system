"""
Веб-сервер с keep-alive для Render.com
Работает параллельно с Telegram ботами
"""
import asyncio
from aiohttp import web
import aiohttp
import os
import logging
import time
from datetime import datetime

logger = logging.getLogger(__name__)

# Глобальная переменная для отслеживания статуса
app_status = {
    "start_time": datetime.now(),
    "last_ping": None,
    "ping_count": 0,
    "bots_active": False
}

async def handle_root(request):
    """Обработчик для корневого URL."""
    logger.info("Received request for /")
    uptime = datetime.now() - app_status["start_time"]
    
    # Добавляем мониторинг ресурсов
    try:
        from resource_monitor import resource_monitor
        from bot_activity_logger import activity_logger
        
        resources = resource_monitor.check_resources()
        daily_activity = activity_logger.get_daily_summary()
        weekly_activity = activity_logger.get_weekly_summary()
        recommendations = resource_monitor.get_recommendations()
    except Exception:
        resources = {"error": "Мониторинг недоступен"}
        daily_activity = {"messages": 0, "ai_requests": 0}
        weekly_activity = {"messages": 0, "ai_requests": 0}
        recommendations = ["Данные недоступны"]
    
    status = {
        "status": "✅ Telegram Userbot System работает!",
        "service": "shlyapa-bot",
        "bots": ["Daniel", "Leonardo", "Алевтина"],
        "environment": "Render.com Production",
        "uptime_seconds": int(uptime.total_seconds()),
        "uptime_readable": str(uptime).split('.')[0],
        "last_ping": app_status["last_ping"].isoformat() if app_status["last_ping"] else None,
        "ping_count": app_status["ping_count"],
        "bots_active": app_status["bots_active"],
        "port": os.environ.get("PORT", "8000"),
        "timestamp": datetime.now().isoformat(),
        "resources": resources,
        "activity_today": daily_activity,
        "activity_week": weekly_activity,
        "recommendations": recommendations
    }
    return web.json_response(status)

async def handle_health(request):
    """Обработчик для проверки здоровья."""
    logger.info("Received request for /health")
    app_status["last_ping"] = datetime.now()
    app_status["ping_count"] += 1
    return web.Response(text="OK")

async def handle_ping(request):
    """Специальный обработчик для self-ping."""
    app_status["last_ping"] = datetime.now()
    app_status["ping_count"] += 1
    return web.json_response({
        "status": "pong",
        "timestamp": datetime.now().isoformat(),
        "ping_count": app_status["ping_count"]
    })

async def self_ping_task():
    """Задача для автоматического пинга каждые 14 минут."""
    await asyncio.sleep(60)  # Ждем минуту после запуска
    
    while True:
        try:
            # Ждем 14 минут (840 секунд)
            await asyncio.sleep(840)
            
            port = os.environ.get("PORT", "8000")
            url = f"http://localhost:{port}/ping"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        logger.info("✅ Self-ping успешен")
                    else:
                        logger.warning(f"⚠️ Self-ping вернул статус {response.status}")
                        
        except Exception as e:
            logger.error(f"❌ Ошибка self-ping: {e}")
            # Продолжаем работать даже при ошибке

def start_web_server():
    """Запускает веб-сервер в отдельной задаче."""
    app = web.Application()
    app.router.add_get('/', handle_root)
    app.router.add_get('/health', handle_health)
    app.router.add_get('/ping', handle_ping)
    
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting web server on port {port}")
    
    runner = web.AppRunner(app)
    asyncio.create_task(runner.setup())
    site = web.TCPSite(runner, '0.0.0.0', port)
    asyncio.create_task(site.start())
    
    # Запускаем задачу self-ping
    asyncio.create_task(self_ping_task())
    
    logger.info(f"Web server started on http://0.0.0.0:{port}")
    logger.info("🔄 Self-ping задача запущена (каждые 14 минут)")
    return runner

if __name__ == "__main__":
    start_web_server()
    
    # Держим сервер активным
    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 Веб-сервер остановлен")
