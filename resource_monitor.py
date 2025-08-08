"""
Мониторинг ресурсов и управление ботами
"""
import psutil
import os
import logging
from datetime import datetime
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class ResourceMonitor:
    def __init__(self):
        self.memory_threshold = 450  # MB (из 512 MB лимита)
        self.cpu_threshold = 80      # %
        self.bot3_disabled = False   # Флаг отключения третьего бота
        
    def get_memory_usage(self) -> float:
        """Возвращает использование памяти в MB"""
        try:
            process = psutil.Process(os.getpid())
            return process.memory_info().rss / 1024 / 1024  # В MB
        except Exception:
            return 0.0
    
    def get_cpu_usage(self) -> float:
        """Возвращает использование CPU в %"""
        try:
            return psutil.cpu_percent(interval=1)
        except Exception:
            return 0.0
    
    def check_resources(self) -> Dict[str, any]:
        """Проверяет ресурсы и возвращает статус"""
        memory_mb = self.get_memory_usage()
        cpu_percent = self.get_cpu_usage()
        
        status = {
            "memory_mb": round(memory_mb, 1),
            "memory_percent": round((memory_mb / 512) * 100, 1),
            "cpu_percent": round(cpu_percent, 1),
            "memory_critical": memory_mb > self.memory_threshold,
            "cpu_critical": cpu_percent > self.cpu_threshold,
            "bot3_disabled": self.bot3_disabled,
            "timestamp": datetime.now().isoformat()
        }
        
        return status
    
    def should_disable_bot3(self) -> bool:
        """Определяет, нужно ли отключить третьего бота"""
        status = self.check_resources()
        
        # Если память критична и бот3 еще не отключен
        if status["memory_critical"] and not self.bot3_disabled:
            logger.warning(f"🚨 Критическое использование памяти: {status['memory_mb']} MB")
            logger.warning(f"🔧 Рекомендуется отключить третьего бота")
            return True
            
        return False
    
    def should_enable_bot3(self) -> bool:
        """Определяет, можно ли включить третьего бота"""
        status = self.check_resources()
        
        # Если память в норме и бот3 отключен
        if not status["memory_critical"] and self.bot3_disabled:
            if status["memory_mb"] < 350:  # Запас в 150 MB
                logger.info(f"✅ Память в норме: {status['memory_mb']} MB")
                logger.info(f"🔧 Можно включить третьего бота")
                return True
                
        return False
    
    def disable_bot3(self):
        """Отключает третьего бота"""
        self.bot3_disabled = True
        logger.warning("🔴 Третий бот отключен для экономии ресурсов")
    
    def enable_bot3(self):
        """Включает третьего бота"""
        self.bot3_disabled = False
        logger.info("🟢 Третий бот включен")
    
    def get_recommendations(self) -> list:
        """Возвращает рекомендации по оптимизации"""
        status = self.check_resources()
        recommendations = []
        
        if status["memory_critical"]:
            recommendations.append("Критическое использование памяти - отключите третьего бота")
        
        if status["cpu_critical"]:
            recommendations.append("Высокая нагрузка CPU - уменьшите частоту AI запросов")
        
        if status["memory_percent"] > 70:
            recommendations.append("Высокое использование памяти - рассмотрите платный план")
        
        if not recommendations:
            recommendations.append("Ресурсы в норме")
        
        return recommendations

# Глобальный экземпляр
resource_monitor = ResourceMonitor()
