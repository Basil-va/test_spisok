# Используем легкий образ Python
FROM python:3.11-slim

# Устанавливаем системные зависимости для Pygame и X11
RUN apt-get update && apt-get install -y \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libx11-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы игры в контейнер
COPY gui.py logic.py /app/

# Устанавливаем зависимость pygame
RUN pip install --no-cache-dir pygame

# Точка входа: запускаем игру через gui.py
CMD ["python", "gui.py"]
