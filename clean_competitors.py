"""
Скрипт для удаления упоминаний конкурентов из всех файлов
"""
import os
import re
import json

# Список конкурентов для удаления
COMPETITORS = [
    'blablacar', 'блаблакар', 'BlaBlaCar', 'БлаБлаКар',
    'uber', 'Uber', 'UBER', 'убер', 'Убер',
    'yandex', 'яндекс', 'Яндекс', 'Yandex',
    'bolt', 'Bolt', 'болт', 'Болт',
    'nas taxi', 'naš taxi', 'Naš taxi', 'HaloTaxi', 'Hello Taxi',
    'red taxi', 'lider taxi', 'pg taxi', 'Pg taxi',
    'TeslaGoApp', 'teslagoapp'
]

def clean_text_file(file_path):
    """Очищает текстовый файл от упоминаний конкурентов"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Удаляем упоминания конкурентов
        for competitor in COMPETITORS:
            # Убираем из списков через запятую
            content = re.sub(rf"['\"]?{re.escape(competitor)}['\"]?,?\s*", '', content, flags=re.IGNORECASE)
            # Заменяем на косвенные упоминания
            content = re.sub(rf"\b{re.escape(competitor)}\b", 'приложение', content, flags=re.IGNORECASE)
        
        # Убираем лишние запятые и пробелы
        content = re.sub(r',\s*,', ',', content)
        content = re.sub(r',\s*]', ']', content)
        content = re.sub(r'\[\s*,', '[', content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Очищен: {file_path}")
        
    except Exception as e:
        print(f"❌ Ошибка в {file_path}: {e}")

def clean_json_file(file_path):
    """Очищает JSON файл от упоминаний конкурентов"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        original_data = json.dumps(data, ensure_ascii=False)
        
        # Рекурсивно очищаем все строки в JSON
        def clean_json_recursive(obj):
            if isinstance(obj, dict):
                return {k: clean_json_recursive(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                cleaned_list = []
                for item in obj:
                    cleaned_item = clean_json_recursive(item)
                    # Проверяем, содержит ли элемент конкурентов
                    if isinstance(cleaned_item, str):
                        has_competitor = any(competitor.lower() in cleaned_item.lower() 
                                           for competitor in COMPETITORS)
                        if not has_competitor:
                            cleaned_list.append(cleaned_item)
                    else:
                        cleaned_list.append(cleaned_item)
                return cleaned_list
            elif isinstance(obj, str):
                cleaned = obj
                for competitor in COMPETITORS:
                    cleaned = re.sub(rf"\b{re.escape(competitor)}\b", 'GO-сервис', cleaned, flags=re.IGNORECASE)
                return cleaned
            else:
                return obj
        
        cleaned_data = clean_json_recursive(data)
        
        if json.dumps(cleaned_data, ensure_ascii=False) != original_data:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
            print(f"✅ Очищен JSON: {file_path}")
        
    except Exception as e:
        print(f"❌ Ошибка в JSON {file_path}: {e}")

def main():
    """Основная функция для очистки всех файлов"""
    print("🧹 Начинаем очистку от упоминаний конкурентов...")
    
    # Файлы для очистки
    files_to_clean = [
        'ai_handler.py',
        'natural_speech_handler.py',
        'bot_prompts.py',
        'quotes.py',
        'gominiapp_topics.py'
    ]
    
    # JSON файлы для очистки
    json_files = [
        'kursor_bot_sasha/natural_speech/conversation_starters.json',
        'kursor_bot_sasha/natural_speech/statements.json',
        'kursor_bot_sasha/natural_speech/questions.json',
        'kursor_bot_sasha/natural_speech/emotional.json'
    ]
    
    # Очищаем Python файлы
    for file_path in files_to_clean:
        if os.path.exists(file_path):
            clean_text_file(file_path)
    
    # Очищаем JSON файлы
    for file_path in json_files:
        if os.path.exists(file_path):
            clean_json_file(file_path)
    
    print("✅ Очистка завершена!")
    print("📝 Все упоминания конкурентов заменены на 'GO-сервис' или удалены")

if __name__ == "__main__":
    main()
