from .scripts.asterisk_connection import AsteriskConnection
import os
from dotenv import load_dotenv

load_dotenv()

def asterisk_connection_status(request):
    # Получаем данные для подключения из настроек или переменных окружения
    host = os.getenv('ASTERISK_HOST')  # IP-адрес сервера
    port = int(os.getenv('ASTERISK_PORT', 22))  # Преобразуем порт в число
    username = os.getenv('ASTERISK_USERNAME')  # Имя пользователя для подключения
    password = os.getenv('ASTERISK_PASSWORD')  # Пароль для подключения

    # Создаем объект подключения к Asterisk
    asterisk_conn = AsteriskConnection(host, port, username, password)

    # Подключаемся к серверу Asterisk
    asterisk_conn.connect()

    # Проверяем соединение
    is_connected = asterisk_conn.check_connection()

    # Закрываем соединение
    asterisk_conn.close_connection()

    # Возвращаем статус подключения
    return {'is_connected': is_connected}