"""
Анализатор сообщений Crazy Cat для создания персонажа Алевтины
"""
import json
import re
from typing import List, Dict

def find_crazy_cat_messages():
    """Находит все сообщения от Crazy Cat в экспорте чата"""
    print("🔍 Анализируем сообщения Crazy Cat...")
    
    try:
        with open('../ChatExport_2025-08-05/result.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        crazy_cat_messages = []
        all_users = set()
        
        for msg in data.get('messages', []):
            if msg.get('type') == 'message':
                from_name = str(msg.get('from', ''))
                from_id = str(msg.get('from_id', ''))
                text = msg.get('text', '')
                
                all_users.add(from_name)
                
                # Ищем по разным вариантам имени
                search_terms = ['crazy cat', 'crazycat', 'алевтина', 'alevtina']
                
                if any(term in from_name.lower() for term in search_terms):
                    if isinstance(text, list):
                        text_str = ''.join([item if isinstance(item, str) else item.get('text', '') for item in text])
                    else:
                        text_str = str(text)
                    
                    if len(text_str.strip()) > 0 and len(text_str) < 300:
                        crazy_cat_messages.append({
                            'text': text_str.strip(),
                            'from_name': from_name,
                            'date': msg.get('date', ''),
                            'id': msg.get('id', 0)
                        })
        
        print(f"📊 Найдено сообщений от Crazy Cat: {len(crazy_cat_messages)}")
        
        # Показываем первые 15 сообщений для анализа
        if crazy_cat_messages:
            print("\n📝 Примеры сообщений Crazy Cat:")
            for i, msg in enumerate(crazy_cat_messages[:15]):
                print(f"{i+1}. {msg['text']}")
        
        # Анализируем стиль общения
        analyze_crazy_cat_style(crazy_cat_messages)
        
        return crazy_cat_messages
        
    except Exception as e:
        print(f"❌ Ошибка при поиске: {e}")
        # Поищем пользователей с похожими именами
        try:
            print("\n🔍 Поиск пользователей с похожими именами...")
            similar_users = [user for user in all_users if any(term in user.lower() for term in ['cat', 'алев', 'crazy'])]
            print(f"Найдено похожих пользователей: {similar_users}")
        except:
            pass
        return []

def analyze_crazy_cat_style(messages: List[Dict]):
    """Анализирует стиль общения Crazy Cat"""
    if not messages:
        return
    
    print("\n🧠 Анализ стиля общения Crazy Cat:")
    
    # Собираем весь текст
    all_text = ' '.join([msg['text'].lower() for msg in messages])
    
    # Анализируем агрессивность
    aggressive_words = ['блять', 'сука', 'дура', 'идиот', 'придурок', 'тупой', 'дебил', 'козел', 'мудак']
    aggressive_count = sum(all_text.count(word) for word in aggressive_words)
    
    # Анализируем вопросительность (придирчивость)
    question_count = all_text.count('?')
    
    # Анализируем негативность
    negative_words = ['плохо', 'ужасно', 'отвратительно', 'кошмар', 'жесть', 'пиздец', 'трындец']
    negative_count = sum(all_text.count(word) for word in negative_words)
    
    # Анализируем честность/прямолинейность
    direct_words = ['честно', 'правда', 'серьезно', 'реально', 'факт']
    direct_count = sum(all_text.count(word) for word in direct_words)
    
    # Часто используемые слова
    words = re.findall(r'\b\w+\b', all_text)
    word_freq = {}
    for word in words:
        if len(word) > 3:  # Только слова длиннее 3 символов
            word_freq[word] = word_freq.get(word, 0) + 1
    
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
    
    print(f"📊 Статистика:")
    print(f"  - Всего сообщений: {len(messages)}")
    print(f"  - Агрессивные слова: {aggressive_count}")
    print(f"  - Вопросы: {question_count}")
    print(f"  - Негативные слова: {negative_count}")
    print(f"  - Прямые слова: {direct_count}")
    print(f"  - Топ слов: {top_words[:5]}")
    
    # Определяем характерные фразы
    print(f"\n💬 Характерные фразы:")
    characteristic_phrases = []
    for msg in messages:
        text = msg['text']
        if any(word in text.lower() for word in aggressive_words + negative_words):
            characteristic_phrases.append(text)
        elif '?' in text and len(text) < 100:
            characteristic_phrases.append(text)
    
    for i, phrase in enumerate(characteristic_phrases[:10]):
        print(f"  {i+1}. {phrase}")

def create_alevtina_character(crazy_cat_messages: List[Dict]):
    """Создает персонажа Алевтины на основе анализа Crazy Cat"""
    
    print("\n👤 Создаем персонажа Алевтины...")
    
    # Извлекаем характерные фразы для использования
    characteristic_phrases = []
    aggressive_phrases = []
    questioning_phrases = []
    
    for msg in crazy_cat_messages:
        text = msg['text']
        if len(text) < 150:  # Короткие фразы
            if '?' in text:
                questioning_phrases.append(text)
            elif any(word in text.lower() for word in ['плохо', 'ужасно', 'что за', 'как так']):
                aggressive_phrases.append(text)
            else:
                characteristic_phrases.append(text)
    
    # Создаем конфигурацию персонажа
    alevtina_config = {
        "name": "Алевтина",
        "age": 30,
        "status": "в разводе с ребенком",
        "car": "невзрачное авто",
        "personality": {
            "aggressiveness": 0.7,
            "honesty": 0.9,
            "criticism": 0.8,
            "mood_spoiler": 0.8
        },
        "characteristic_phrases": characteristic_phrases[:20],
        "aggressive_phrases": aggressive_phrases[:15],
        "questioning_phrases": questioning_phrases[:15]
    }
    
    # Сохраняем конфигурацию
    import os
    os.makedirs('alevtina', exist_ok=True)
    os.makedirs('alevtina/data', exist_ok=True)
    
    with open('alevtina/data/character_config.json', 'w', encoding='utf-8') as f:
        json.dump(alevtina_config, f, ensure_ascii=False, indent=2)
    
    print("✅ Конфигурация Алевтины создана в alevtina/data/character_config.json")
    
    return alevtina_config

if __name__ == "__main__":
    messages = find_crazy_cat_messages()
    if messages:
        create_alevtina_character(messages)
    else:
        print("⚠️ Сообщения Crazy Cat не найдены. Создаем персонажа на основе описания...")
        # Создаем базовый персонаж
        base_config = {
            "name": "Алевтина", 
            "age": 30,
            "status": "в разводе с ребенком",
            "car": "невзрачное авто",
            "personality": {
                "aggressiveness": 0.7,
                "honesty": 0.9,
                "criticism": 0.8,
                "mood_spoiler": 0.8
            }
        }
        import os
        os.makedirs('alevtina/data', exist_ok=True)
        with open('alevtina/data/character_config.json', 'w', encoding='utf-8') as f:
            json.dump(base_config, f, ensure_ascii=False, indent=2)
        print("✅ Базовая конфигурация Алевтины создана")