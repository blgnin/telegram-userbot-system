"""
Модуль для интеграции естественной речи из реальных диалогов
в систему ботов для более человечного общения
"""
import json
import random
import os
from typing import Dict, List, Optional
from pathlib import Path

class NaturalSpeechHandler:
    def __init__(self, natural_speech_dir: str = None):
        if natural_speech_dir is None:
            # Получаем путь к директории текущего файла
            current_dir = Path(__file__).parent
            self.natural_speech_dir = str(current_dir / "natural_speech")
        else:
            self.natural_speech_dir = natural_speech_dir
        self.speech_data = {}
        self.load_natural_speech_data()
        
    def load_natural_speech_data(self):
        """Загружает данные естественной речи из файлов"""
        try:
            if not os.path.exists(self.natural_speech_dir):
                print(f"Папка {self.natural_speech_dir} не найдена. Запустите сначала chat_parser.py")
                return
            
            categories = ['general', 'questions', 'statements', 'emotional', 'conversation_starters']
            
            for category in categories:
                file_path = os.path.join(self.natural_speech_dir, f"{category}.json")
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        self.speech_data[category] = data.get('messages', [])
                        print(f"Загружено {len(self.speech_data[category])} сообщений: {category}")
                else:
                    self.speech_data[category] = []
                    print(f"Файл не найден: {file_path}")
            
            total_messages = sum(len(messages) for messages in self.speech_data.values())
            print(f"Всего загружено естественных сообщений: {total_messages}")
            
        except Exception as e:
            print(f"Ошибка при загрузке естественной речи: {e}")
            self.speech_data = {cat: [] for cat in ['general', 'questions', 'statements', 'emotional', 'conversation_starters']}
    
    def get_natural_response(self, message: str, bot_name: str, context: str = "") -> Optional[str]:
        """
        Возвращает естественный ответ на основе реальных диалогов
        """
        try:
            message_lower = message.lower()
            
            # Определяем категорию ответа на основе входящего сообщения
            response_category = self._determine_response_category(message_lower, context)
            
            # Получаем подходящие ответы
            candidate_responses = self.speech_data.get(response_category, [])
            
            if not candidate_responses:
                # Если нет подходящих ответов в основной категории, пробуем общие
                candidate_responses = self.speech_data.get('general', [])
            
            if not candidate_responses:
                return None
            
            # Фильтруем ответы по релевантности к теме поездок/приложения
            relevant_responses = self._filter_relevant_responses(candidate_responses, message_lower, context)
            
            if not relevant_responses:
                # Если нет релевантных ответов, используем общие короткие фразы
                relevant_responses = [resp for resp in candidate_responses if len(resp) < 50][:10]
            
            if not relevant_responses:
                return None
            
            # Выбираем случайный ответ и адаптируем его под персонажа
            natural_response = random.choice(relevant_responses)
            adapted_response = self._adapt_response_to_character(natural_response, bot_name)
            
            return adapted_response
            
        except Exception as e:
            print(f"Ошибка при генерации естественного ответа: {e}")
            return None
    
    def _filter_relevant_responses(self, responses: List[str], message_lower: str, context: str) -> List[str]:
        """Фильтрует ответы по релевантности к теме поездок и приложения"""
        travel_keywords = [
            # Поездки и транспорт
            'поездка', 'поездки', 'ехать', 'едем', 'ездить', 'дорога', 'путь', 'маршрут',
            'водитель', 'пассажир', 'машина', 'авто', 'такси', 'трансфер', 'попутка',
            'автобус', 'поезд', 'самолет', 'метро', 'транспорт', 'переезд',
            # Цены и оплата
            'цена', 'стоимость', 'тариф', 'деньги', 'рубл', 'евро', 'доллар', 
            'дешево', 'дорого', 'скидка', 'акция', 'оплата', 'карта', 'наличные',
            # Время и скорость
            'время', 'быстро', 'долго', 'час', 'минут', 'утром', 'вечером', 
            'срочно', 'медленно', 'опоздать', 'успеть', 'вовремя',
            # Места и локации
            'город', 'аэропорт', 'вокзал', 'центр', 'район', 'адрес', 'место',
            'дом', 'работа', 'офис', 'магазин', 'больница', 'отель',
            # Качество сервиса
            'удобно', 'комфорт', 'безопасно', 'надежно', 'качество', 'сервис',
            'отзыв', 'рейтинг', 'рекомендую', 'советую', 'хороший', 'плохой',
            # Приложение и технологии
            'приложение', 'аппка', 'программа', 'телефон', 'заказ', 'бронь',
            'кнопка', 'экран', 'интерфейс', 'уведомление', 'смс', 'звонок',
            # GO-сервис специфика
            'gominiapp', 'гомини', 'го сервис', 'токен', 'премиум', 'рейтинг',
            'попутчик', 'мини-приложение', 'telegram',
            'бот', 'чат', 'сообщение', 'остановка', 'промежуточный', 'точка',
            'регистрация', 'профиль', 'настройки', 'роль', 'статус'
        ]
        
        # Проверяем релевантность ответов
        relevant = []
        for response in responses:
            response_lower = response.lower()
            
            # Проверяем наличие ключевых слов
            has_travel_words = any(keyword in response_lower for keyword in travel_keywords)
            
            # Проверяем длину (предпочитаем короткие и средние ответы)
            is_good_length = 10 <= len(response) <= 100
            
            # Исключаем неподходящие ответы (не связанные с поездками)
            bad_patterns = [
                'кипс', 'кип', 'странно', 'непонятно', 'хз', 'не знаю что это',
                'музыка', 'песня', 'фильм', 'кино', 'игра', 'спорт', 'футбол',
                'еда', 'готовить', 'рецепт', 'ресторан', 'кафе', 'бар',
                'работа не по теме', 'учеба', 'школа', 'университет', 'экзамен',
                'погода просто так', 'дождь без контекста', 'снег без контекста',
                'zara', 'bulevar', 'vlahovića', 'магазин одежды', 'шопинг', 'покупки',
                'википедия', 'wikipedia', 'ссылка', 'сайт', 'интернет без контекста',
                'личная жизнь', 'отношения без контекста', 'любовь без контекста'
            ]
            has_bad_patterns = any(bad in response_lower for bad in bad_patterns)
            
            if (has_travel_words or is_good_length) and not has_bad_patterns:
                relevant.append(response)
        
        return relevant[:20]  # Ограничиваем количество
    
    def _determine_response_category(self, message_lower: str, context: str) -> str:
        """Определяет категорию ответа на основе входящего сообщения"""
        
        # Если сообщение - вопрос, отвечаем утверждением
        if any(word in message_lower for word in ['что', 'как', 'где', 'когда', 'почему', 'зачем', '?']):
            return 'statements'
        
        # Если сообщение эмоциональное, отвечаем эмоционально
        emotional_words = ['круто', 'отлично', 'супер', 'офигеть', 'вау', 'блин', 'черт', 'капец', 'жесть']
        if any(word in message_lower for word in emotional_words):
            return 'emotional'
        
        # Если это начало разговора, отвечаем дружелюбно
        if any(word in message_lower for word in ['привет', 'здравствуй', 'добр', 'салют']):
            return 'conversation_starters'
        
        # По умолчанию - общие ответы
        return 'general'
    
    def _adapt_response_to_character(self, response: str, bot_name: str) -> str:
        """Адаптирует ответ под характер конкретного бота"""
        
        if "Leonardo" in bot_name:
            # Leonardo - пассажир, душный, экономный
            response = self._add_leonardo_flavor(response)
        elif "Daniel" in bot_name:
            # Daniel - водитель, уверенный, с Lexus
            response = self._add_daniel_flavor(response)
        elif "Алевтина" in bot_name or "алевтина" in bot_name:
            # Алевтина - критик, агрессивная, недовольная
            response = self._add_alevtina_flavor(response)
        
        # Обрезаем до разумной длины (максимум 150 символов)
        if len(response) > 150:
            sentences = response.split('.')
            if sentences:
                response = sentences[0] + '.'
        
        return response
    
    def _add_leonardo_flavor(self, response: str) -> str:
        """Добавляет характерные черты Leonardo к ответу"""
        
        # Словарь замен для Leonardo (пассажир, экономный)
        leonardo_replacements = {
            'машина': 'попутка',
            'поехали': 'добираемся',
            'дорого': 'для меня дорого',
            'классно': 'норм, но дорого',
            'отлично': 'неплохо, если по карману'
        }
        
        # Применяем замены
        for old, new in leonardo_replacements.items():
            response = response.replace(old, new)
        
        return response
    
    def _add_daniel_flavor(self, response: str) -> str:
        """Добавляет характерные черты Daniel к ответу"""
        
        # Словарь замен для Daniel (водитель, с Lexus)
        daniel_replacements = {
            'машина': 'Lexus',
            'тачка': 'Lexus',
            'авто': 'Lexus'
        }
        
        # Применяем замены
        for old, new in daniel_replacements.items():
            response = response.replace(old, new)
        
        return response
    
    def _add_alevtina_flavor(self, response: str) -> str:
        """Добавляет характерные черты Алевтины к ответу"""
        
        # Словарь замен для Алевтины (критик, агрессивная)
        alevtina_replacements = {
            'хорошо': 'нормально',
            'отлично': 'ну и что',
            'супер': 'ну да, конечно',
            'классно': 'ага, как же',
            'круто': 'и что с того',
            'прекрасно': 'ну и дела',
            'замечательно': 'ну да, замечательно'
        }
        
        # Применяем замены
        for old, new in alevtina_replacements.items():
            response = response.replace(old, new)
        
        return response
    
    def get_conversation_starter(self, bot_name: str) -> str:
        """Возвращает естественное начало разговора"""
        starters = self.speech_data.get('conversation_starters', [])
        
        if not starters:
            # Запасные варианты, если нет данных
            if "Leonardo" in bot_name:
                return "Народ, как дела с попутками?"
            elif "Алевтина" in bot_name or "алевтина" in bot_name:
                return "Опять что-то новое придумали? И что это за херня?"
            else:
                return "Ребят, кто куда едет?"
        
        starter = random.choice(starters)
        return self._adapt_response_to_character(starter, bot_name)
    
    def enhance_ai_response(self, ai_response: str, bot_name: str) -> str:
        """Улучшает AI ответ, добавляя естественности"""
        try:
            # Если AI ответ слишком формальный, заменяем его естественным
            formal_indicators = [
                'я думаю', 'считаю что', 'полагаю', 'мне кажется',
                'по моему мнению', 'с моей точки зрения'
            ]
            
            if any(indicator in ai_response.lower() for indicator in formal_indicators):
                # Попробуем найти более естественную альтернативу
                natural_alternative = self.get_natural_response("", bot_name)
                if natural_alternative and len(natural_alternative) > 10:
                    return natural_alternative
            
            return ai_response
            
        except Exception as e:
            print(f"Ошибка при улучшении AI ответа: {e}")
            return ai_response
    
    def get_statistics(self) -> Dict[str, int]:
        """Возвращает статистику по загруженным данным"""
        return {category: len(messages) for category, messages in self.speech_data.items()}

# Глобальный экземпляр для использования в других модулях
natural_speech = NaturalSpeechHandler()