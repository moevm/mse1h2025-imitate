# Настройка и запуск

- создать виртуальное окружение (в главной директории проекта, которая написана ***ЧЕРЕЗ ТИРЕ***: `mse1h2025-imitate`)
- активировать виртуальное окружение (`venv/Scripts/activate` или `venv/bin/activate`)
- обновить менеджер пакетов `python -m pip install --upgrade pip`
- установить зависимости - `pip install -r requirements.txt`
- создать в той же главной папке проекта, что и venv файл `.env` и поместите туда DJANGO_SECRET_KEY (запросить у сокомандников)

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
├── README.md
├── requirements.txt            зависимости
├── .env                        файл с информацией
└── venv/                       виртуальное окружение
```
