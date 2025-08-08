"""
Система логирования активности ботов для мониторинга
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List

class BotActivityLogger:
    def __init__(self):
        self.activity_file = "bot_activity.json"
        self.stats = self.load_stats()
    
    def load_stats(self) -> Dict:
        """Загружает статистику из файла"""
        try:
            if os.path.exists(self.activity_file):
                with open(self.activity_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        
        return {
            "daily_stats": {},
            "total_messages": 0,
            "total_ai_requests": 0,
            "last_activity": None,
            "uptime_start": datetime.now().isoformat()
        }
    
    def save_stats(self):
        """Сохраняет статистику в файл"""
        try:
            with open(self.activity_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    
    def log_message(self, bot_name: str, message_type: str = "reply"):
        """Логирует отправленное сообщение"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        if today not in self.stats["daily_stats"]:
            self.stats["daily_stats"][today] = {
                "messages": 0,
                "ai_requests": 0,
                "bots": {}
            }
        
        if bot_name not in self.stats["daily_stats"][today]["bots"]:
            self.stats["daily_stats"][today]["bots"][bot_name] = 0
        
        self.stats["daily_stats"][today]["messages"] += 1
        self.stats["daily_stats"][today]["bots"][bot_name] += 1
        self.stats["total_messages"] += 1
        self.stats["last_activity"] = datetime.now().isoformat()
        
        self.save_stats()
    
    def log_ai_request(self):
        """Логирует AI запрос"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        if today not in self.stats["daily_stats"]:
            self.stats["daily_stats"][today] = {
                "messages": 0,
                "ai_requests": 0,
                "bots": {}
            }
        
        self.stats["daily_stats"][today]["ai_requests"] += 1
        self.stats["total_ai_requests"] += 1
        
        self.save_stats()
    
    def get_daily_summary(self) -> Dict:
        """Возвращает сводку за сегодня"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        if today in self.stats["daily_stats"]:
            return self.stats["daily_stats"][today]
        
        return {"messages": 0, "ai_requests": 0, "bots": {}}
    
    def get_weekly_summary(self) -> Dict:
        """Возвращает сводку за неделю"""
        week_ago = datetime.now() - timedelta(days=7)
        total_messages = 0
        total_ai_requests = 0
        
        for date_str, stats in self.stats["daily_stats"].items():
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d")
                if date >= week_ago:
                    total_messages += stats.get("messages", 0)
                    total_ai_requests += stats.get("ai_requests", 0)
            except ValueError:
                continue
        
        return {
            "messages": total_messages,
            "ai_requests": total_ai_requests,
            "period": "7 days"
        }
    
    def cleanup_old_data(self):
        """Удаляет данные старше 30 дней"""
        cutoff_date = datetime.now() - timedelta(days=30)
        
        to_remove = []
        for date_str in self.stats["daily_stats"]:
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d")
                if date < cutoff_date:
                    to_remove.append(date_str)
            except ValueError:
                to_remove.append(date_str)
        
        for date_str in to_remove:
            del self.stats["daily_stats"][date_str]
        
        if to_remove:
            self.save_stats()

# Глобальный экземпляр
activity_logger = BotActivityLogger()
