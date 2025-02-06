import paramiko
import os
import json
from dotenv import load_dotenv

load_dotenv()


class CallingNumber:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def get_active_calls(self):
        """ Получает активные звонки и номера звонящих с Asterisk """
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self.host, port=self.port, username=self.username, password=self.password)

            stdin, stdout, stderr = client.exec_command('asterisk -rx "core show channels verbose"')

            call_info = stdout.read().decode()
            error_info = stderr.read().decode()

            if error_info:
                return {"error": f"Ошибка: {error_info}"}

            # Извлекаем номера звонящих
            calling_numbers = self.extract_calling_numbers(call_info)

            if calling_numbers:
                print("Входящие номера:")
                for number in calling_numbers:
                    print(number)
            else:
                print("Нет активных звонков.")

            return {"calling_numbers": calling_numbers}

        except Exception as e:
            return {"error": str(e)}

        finally:
            client.close()

    def extract_calling_numbers(self, call_info):
        """
        Разбирает вывод `core show channels verbose` и извлекает номера звонящих.
        """
        calling_numbers = []

        for line in call_info.splitlines():
            parts = line.split()
            if len(parts) >= 8:  # В Asterisk CallerID обычно находится в 7-8 колонке
                caller_id = parts[7]
                if caller_id.isdigit():
                    calling_numbers.append(caller_id)

        return calling_numbers


# Создаем объект
calling_number = CallingNumber(
    os.getenv("ASTERISK_HOST"),
    int(os.getenv("ASTERISK_PORT", 22)),
    os.getenv("ASTERISK_USERNAME"),
    os.getenv("ASTERISK_PASSWORD")
)

# Получаем и печатаем входящие звонки
calling_number.get_active_calls()
