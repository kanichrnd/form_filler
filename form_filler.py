import requests
import json
import os
import sys

def load_config():
    # Получаем путь к директории, где находится исполняемый файл
    if getattr(sys, 'frozen', False):
        # Если это exe файл
        application_path = os.path.dirname(sys.executable)
    else:
        # Если это python скрипт
        application_path = os.path.dirname(os.path.abspath(__file__))
    
    config_path = os.path.join(application_path, 'config.json')
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл конфигурации не найден: {config_path}")
        print("Создаю новый файл config.json...")
        default_config = {"name": ""}  # Создаем с пустым значением
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4, ensure_ascii=False)
        print("Пожалуйста, укажите ваше имя в файле config.json и запустите программу снова.")
        input("Нажмите Enter для выхода...")
        sys.exit(0)  # Завершаем программу после создания файла
    except json.JSONDecodeError:
        print("Ошибка в файле конфигурации. Использую пустое значение.")
        return {"name": ""}

# URL для Google формы
GoogleURL = 'https://docs.google.com/forms/u/0/d/e/1FAIpQLScnPlxdVkDzVJgcRYlXVDCzrfb768uKgbZYRBd7vUJKQ-alGA'
urlResponse = GoogleURL + '/formResponse'
urlReferer = GoogleURL + '/viewform'

def submit_form():
    # Загружаем конфигурацию
    config = load_config()
    name = config.get('name', '').strip()  # Удаляем пробелы в начале и конце
    
    # Проверяем, что поле name не пустое
    if not name:
        print("Ошибка: поле 'name' в файле config.json не может быть пустым!")
        print("Пожалуйста, укажите значение в файле config.json")
        input("Нажмите Enter для выхода...")
        return False
    
    form_data = {
        'entry.129254320': name,
    }
    
    user_agent = {
        'Referer': urlReferer,
        'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36"
    }
    
    try:
        r = requests.post(urlResponse, data=form_data, headers=user_agent)
        if r.status_code == 200:
            print(f"Форма успешно отправлена для пользователя: {name}")
            return True
        else:
            print(f"Ошибка при отправке формы. Код ответа: {r.status_code}")
            return False
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        return False

if __name__ == "__main__":
    submit_form()
    input("Нажмите Enter для выхода...")