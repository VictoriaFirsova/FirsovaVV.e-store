# Используем официальный Python образ
FROM python:3.12-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем содержимое проекта в рабочую директорию контейнера
COPY . .

# Указываем команду для запуска FastAPI приложения
CMD ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8001"]