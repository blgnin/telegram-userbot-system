# Используем официальный Python образ
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы требований
COPY "kursor bot sasha/requirements.txt" ./requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Устанавливаем рабочую директорию для запуска
WORKDIR /app/kursor bot sasha

# Команда запуска
CMD ["python", "main_userbot.py"]