"""
Парсер экспорта чата для извлечения естественных диалогов
и интеграции их в базу знаний ботов
"""
import json
import re
import random
from typing import List, Dict, Any
from datetime import datetime

class ChatParser:
    def __init__(self, chat_export_path: str):
        self.chat_export_path = chat_export_path
        self.natural_responses = {
            'general': [],
            'questions': [],
            'statements': [],
            'emotional': [],
            'conversation_starters': []
        }
        
    def parse_chat_export(self) -> Dict[str, List[str]]:
        """Парсит экспорт чата и извлекает естественные диалоги"""
        try:
            print(f"🔄 Загружаем экспорт чата: {self.chat_export_path}")
            
            with open(self.chat_export_path, 'r', encoding='utf-8') as f:
                chat_data = json.load(f)
            
            messages = chat_data.get('messages', [])
            print(f"📊 Найдено сообщений: {len(messages)}")
            
            # Фильтруем и анализируем сообщения
            self._analyze_messages(messages)
            
            return self.natural_responses
            
        except Exception as e:
            print(f"❌ Ошибка при парсинге чата: {e}")
            return {}
    
    def _analyze_messages(self, messages: List[Dict[str, Any]]):
        """Анализирует сообщения и классифицирует их"""
        processed_count = 0
        
        for msg in messages:
            # Пропускаем служебные сообщения
            if msg.get('type') != 'message':
                continue
                
            text = self._extract_text(msg)
            if not text or len(text) < 5:
                continue
            
            # Очищаем текст
            clean_text = self._clean_text(text)
            if not clean_text:
                continue
            
            # Классифицируем сообщение
            self._classify_message(clean_text)
            processed_count += 1
            
            if processed_count % 1000 == 0:
                print(f"📝 Обработано сообщений: {processed_count}")
        
        print(f"✅ Всего обработано: {processed_count}")
        self._print_statistics()
    
    def _extract_text(self, msg: Dict[str, Any]) -> str:
        """Извлекает текст из сообщения"""
        text = msg.get('text', '')
        
        # Если text - это список (с форматированием)
        if isinstance(text, list):
            text_parts = []
            for item in text:
                if isinstance(item, str):
                    text_parts.append(item)
                elif isinstance(item, dict) and 'text' in item:
                    text_parts.append(item['text'])
            text = ''.join(text_parts)
        
        return str(text).strip()
    
    def _clean_text(self, text: str) -> str:
        """Очищает текст от лишних символов и форматирования"""
        # Убираем ссылки
        text = re.sub(r'http[s]?://\S+', '', text)
        
        # Убираем упоминания пользователей
        text = re.sub(r'@\w+', '', text)
        
        # Убираем хештеги
        text = re.sub(r'#\w+', '', text)
        
        # Убираем множественные пробелы
        text = re.sub(r'\s+', ' ', text)
        
        # Убираем слишком длинные сообщения (более 200 символов)
        if len(text) > 200:
            return ""
        
        # Убираем сообщения только из эмодзи
        if re.match(r'^[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\s]+$', text):
            return ""
        
        return text.strip()
    
    def _classify_message(self, text: str):
        """Классифицирует сообщение по типу"""
        text_lower = text.lower()
        
        # Вопросы
        question_patterns = [
            r'\?', r'как\s+', r'что\s+', r'где\s+', r'когда\s+', 
            r'почему\s+', r'зачем\s+', r'кто\s+'
        ]
        
        if any(re.search(pattern, text_lower) for pattern in question_patterns):
            self.natural_responses['questions'].append(text)
            return
        
        # Эмоциональные сообщения
        emotional_words = [
            'круто', 'отлично', 'супер', 'класс', 'офигеть', 'вау', 
            'блин', 'черт', 'капец', 'жесть', 'обожаю', 'ненавижу',
            'прикольно', 'здорово', 'бомба', 'огонь'
        ]
        
        if any(word in text_lower for word in emotional_words):
            self.natural_responses['emotional'].append(text)
            return
        
        # Начала разговоров
        starter_patterns = [
            r'^привет', r'^здравствуй', r'^добр', r'^ребят', 
            r'^народ', r'^слушай', r'^кстати'
        ]
        
        if any(re.search(pattern, text_lower) for pattern in starter_patterns):
            self.natural_responses['conversation_starters'].append(text)
            return
        
        # Обычные утверждения
        if len(text.split()) > 2 and not text.endswith('?'):
            self.natural_responses['statements'].append(text)
        else:
            self.natural_responses['general'].append(text)
    
    def _print_statistics(self):
        """Выводит статистику по найденным сообщениям"""
        print("\n📊 Статистика извлеченных сообщений:")
        for category, messages in self.natural_responses.items():
            print(f"  {category}: {len(messages)}")
    
    def get_random_response(self, category: str = 'general') -> str:
        """Возвращает случайный ответ из указанной категории"""
        responses = self.natural_responses.get(category, [])
        return random.choice(responses) if responses else ""
    
    def save_to_files(self, output_dir: str = "kursor bot sasha/"):
        """Сохраняет извлеченные данные в файлы"""
        try:
            import os
            
            # Создаем папку для естественной речи
            natural_speech_dir = os.path.join(output_dir, "natural_speech")
            os.makedirs(natural_speech_dir, exist_ok=True)
            
            # Сохраняем каждую категорию в отдельный файл
            for category, messages in self.natural_responses.items():
                if messages:
                    filename = os.path.join(natural_speech_dir, f"{category}.json")
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump({
                            'category': category,
                            'count': len(messages),
                            'messages': messages
                        }, f, ensure_ascii=False, indent=2)
                    
                    print(f"💾 Сохранено {len(messages)} сообщений в {filename}")
            
            print(f"✅ Все данные сохранены в {natural_speech_dir}")
            
        except Exception as e:
            print(f"❌ Ошибка при сохранении: {e}")

if __name__ == "__main__":
    # Пример использования
    parser = ChatParser("../ChatExport_2025-08-05/result.json")
    natural_data = parser.parse_chat_export()
    parser.save_to_files()