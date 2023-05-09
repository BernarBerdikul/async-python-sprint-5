## Базовый образ для сборки
FROM python:3.11.1-slim

# Указываем рабочую директорию
WORKDIR /app

# Запрещаем Python писать файлы .pyc на диск
ENV PYTHONDONTWRITEBYTECODE 1
# Запрещает Python буферизовать stdout и stderr
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        python3-dev \
        libpq-dev \
    # clean
    && rm -rf /root/.cache \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get -qq autoremove \
    && apt-get clean

# Установка зависимостей проекта
COPY ./requirements.txt ./alembic.ini ./entrypoint.sh ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

# Копируем проект
COPY ./src ./src
