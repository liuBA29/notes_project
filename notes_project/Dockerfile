#Dockerfile

# Используем базовый Python-образ
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости проекта
COPY requirements.txt /app/requirements.txt

# Устанавливаем зависимости
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Копируем все файлы проекта
COPY . /app

# Собираем статические файлы (при сборке контейнера)
RUN python manage.py collectstatic --noinput

# Указываем порт, который будет использоваться приложением
EXPOSE 8000

# Указываем команду запуска Gunicorn
CMD ["gunicorn", "notes_project.wsgi:application", "--bind", "0.0.0.0:8000"]
