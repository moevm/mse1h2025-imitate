# Настройка и запуск

## Общие данные
- версия python - 3.9
- создать виртуальное окружение (в главной директории проекта, которая написана ***ЧЕРЕЗ ТИРЕ***: `mse1h2025-imitate`) (`python -m venv venv` или `python3 -m venv venv`)
- активировать виртуальное окружение (`venv/Scripts/activate` или `venv/bin/activate`)
- обновить менеджер пакетов `python -m pip install --upgrade pip` (`pip install --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt`)
- установить зависимости - `pip install -r requirements.txt`
- создать в той же главной папке проекта, что и venv файл `.env` и поместите туда все креды (запросить у сокомандников) (DJANGO_SECRET_KEY - генерируется джанго при создании проекта, либо в терминале - `python manage.py shell`, `from django.core.management import utils`, `utils.get_random_secret_key()`; DB_NAME, DB_USER, DB_PASSWORD - создаются для БД самостоятельно)
- запуск `python manage.py runserver`, когда вы находитесь в папке django-проекта `mse1h2025_imitate` (***ЧЕРЕЗ ПОДЧЁРКИВАНИЕ***)

## Запуск с учетом docker-compose.yaml
- Также необходимо создать в корневой директории .env и положить туда данные. Данные заданы отдельно (запросить у сокомандников).
- Для запуска проекта использовать команду (`docker-compose up --build`). В случае ошибок проследить логи в терминале. Выполнять эти операции из корневой директории (там, где лежит .env и docker-compose.yaml).
- При запуске может возникнуть ошибка следующего характера: на сайте висит ошибка подключения, в логах же при этом все хорошо. В таком случае проблема может быть связана с портом `5432` (порт для db). Для решения следует поменять порт на другой. Сделать это можно в `docker-compose.yaml`.

## Запуск тестов
- для запуска тестов после поднятия докеров необходимо войти в докер бакенда с помощью команды `docker exec -it django_backend bash`
- запуск тестов производится в директории mse1h2025_imitate/mse1h2025_imitate на одном уровне с директорией tests
- для запуска всех тестов нужно ввести команду `pytest -v`
- для запуска тестов регистрации и авторизации `pytest tests/test_registration_and_authorization_api.py -v` 
- для запуска тестов парсинга презентаций `pytest tests/test_presentation_parser.py -v`
- для запуска тестов сервиса TTS `pytest tests/test_tts_service.py -v`
- если необходимо запустить отдельный тест, например test_reg_and_auth_api_must_fail_if_user_not_logged_in в tests/test_registration_and_authorization_api.py, то нужно указать следующую команду `pytest tests/test_registration_and_authorization_api.py -k test_reg_and_auth_api_must_fail_if_user_not_logged_in -v`

# При деплое  
Убрать `Debug = True` из `mse1h2025_imitate/mse1h2025_imitate/setting.py`



Итоговая иерархия проекта:

```
mse1h2025-imitate/              директория проекта (через ТИРЕ)
├── mse1h2025_imitate/          папка Django-проекта (через ПОДЧЁРКИВАНИЕ)
│   ├── backend/                приложение для обработки логики
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   └── views.py
│   ├── manage.py
│   ├── mse1h2025_imitate/      главное приложение проекта (через ПОДЧЁРКИВАНИЕ)
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── users_manager/          приложение для управления пользователями
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── migrations/
│       │   └── __init__.py
│       ├── models.py
│       ├── tests.py
│       └── views.py
├── venv/                       виртуальное окружение
├── .dockerignore
├── .env                        файл с информацией окружения
├── .gitignore
├── docker-compose.yaml
├── Dockerfile
├── README.md
└── requirements.txt            зависимости библиотек python
```