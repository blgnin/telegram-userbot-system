FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Устанавливаем переменную окружения для Python
ENV PYTHONPATH=/app

# Открываем порт
EXPOSE 8000

# Команда запуска (для Fly.io используем main.py)
CMD ["python", "main.py"]