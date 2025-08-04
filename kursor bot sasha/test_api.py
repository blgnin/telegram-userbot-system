import os
from dotenv import load_dotenv
import openai

# Загружаем переменные окружения из правильного файла
load_dotenv('shlyapa1.env')

# Получаем API ключ
api_key = os.getenv('OPENAI_API_KEY')
print(f"API ключ загружен: {'Да' if api_key and api_key != 'your_openai_api_key_here' else 'Нет'}")
print(f"API ключ: {api_key[:10]}..." if api_key and api_key != 'your_openai_api_key_here' else "API ключ не найден")

# Настраиваем OpenAI
openai.api_key = api_key

async def test_openai():
    try:
        print("Тестируем OpenAI API...")
        client = openai.AsyncOpenAI(api_key=api_key)
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Привет! Как дела?"}
            ],
            max_tokens=50
        )
        print("✅ API работает!")
        print(f"Ответ: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"❌ Ошибка API: {e}")
        return False

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_openai()) 