# Полное руководство по развертыванию проекта MSE1H2025 Imitate

## Требования
- Docker и Docker Compose (для Docker-развертывания)
- Python 3.9 (для локальной разработки без Docker)

## 1. Настройка окружения

1. Создайте файл `.env` в корне проекта с содержимым:
```
DJANGO_SECRET_KEY=секретный ключ
DB_NAME=имя базы данных
DB_USER=пользователь
DB_PASSWORD=пароль бд
DATABASE_HOST=db
DATABASE_PORT=5432
```

2. Для генерации нового Django secret key выполните:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 2. Запуск с помощью Docker (рекомендуемый способ)

1. Соберите и запустите контейнеры:
```bash
docker-compose up --build
```

2. После первого запуска создайте суперпользователя:
```bash
docker exec -it django_backend python manage.py createsuperuser
```

3. Приложение будет доступно по адресу: http://localhost:8000

## 3. Локальная разработка (без Docker)

1. Создайте и активируйте виртуальное окружение:
```bash
# Windows:
python -m venv venv
venv\Scripts\activate
# Linux/Mac:
python3 -m venv venv
source venv/bin/activate
```

2. Установите зависимости:
```bash
pip install --upgrade pip
pip install --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt
```

3. Настройте базу данных и запустите сервер:
```bash
python manage.py migrate
python manage.py runserver
```

## 4. Запуск тестов

1. Войдите в контейнер backend:
```bash
docker exec -it django_backend bash
```

2. Запустите тесты:
```bash
# Все тесты
pytest -v

# Конкретные тесты:
pytest tests/test_registration_and_authorization_api.py -v
pytest tests/test_presentation_parser.py -v
pytest tests/test_tts_service.py -v

# Конкретный тест:
pytest tests/test_file.py::TestClass::test_method -v
```

## 5. Деплой в production

1. Обязательные изменения перед деплоем:
- В `graduate_imitator/config/settings.py` установите:
  ```python
  DEBUG = False
  ALLOWED_HOSTS = ['ваш-домен.ru', 'ip-адрес']
  ```

2. Рекомендации для production:
- Используйте отдельный файл `docker-compose.prod.yml`
- Замените `runserver` на Gunicorn/Uvicorn
- Настройте правильную обработку статических файлов
- Используйте HTTPS
- Настройте мониторинг и логирование

## 6. Полезные команды

- Остановка контейнеров: `docker-compose down`
- Просмотр логов: `docker-compose logs -f`
- Пересборка без кеша: `docker-compose build --no-cache`
- Очистка Docker: `docker system prune -a`