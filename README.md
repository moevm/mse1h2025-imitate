# Настройка и запуск

- версия python - 3.9
- создать виртуальное окружение (в главной директории проекта, которая написана ***ЧЕРЕЗ ТИРЕ***: `mse1h2025-imitate`) (`python -m venv venv` или `python3 -m venv venv`)
- активировать виртуальное окружение (`venv/Scripts/activate` или `venv/bin/activate`)
- обновить менеджер пакетов `python -m pip install --upgrade pip`
- установить зависимости - `pip install -r requirements.txt`
- создать в той же главной папке проекта, что и venv файл `.env` и поместите туда все креды (запросить у сокомандников) (DJANGO_SECRET_KEY - генерируется джанго при создании проекта, будет передан командой после сдачи проекта, DB_NAME, DB_USER, DB_PASSWORD - создаются для БД самостоятельно)
- запуск `python manage.py runserver`, когда вы находитесь в папке django-проекта `mse1h2025_imitate` (***ЧЕРЕЗ ПОДЧЁРКИВАНИЕ***)

# При деплое  
Убрать `Debug = True` из `mse1h2025_imitate/mse1h2025_imitate/setting.py`


Итог:

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
├── .env                        файл с информацией окружения
├── .gitignore
├── docker-compose.yaml
├── README.md
└── requirements.txt            зависимости библиотек python
```
