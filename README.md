# Coursework 5 — Habit Tracker

Бэкенд SPA-приложения для трекинга полезных привычек (по мотивам книги «Атомные привычки»).

## Стек
- Python 3.12+
- Django 5.2, Django REST Framework
- SimpleJWT (аутентификация)
- Celery + django-celery-beat (напоминания)
- Telegram Bot API (уведомления)
- drf-spectacular (документация)
- Poetry (зависимости)

## Установка

1. Клонировать репозиторий и перейти в папку:
   ```bash
   git clone <url>
   cd coursework_5
   ```

2. Установить зависимости:
   ```bash
   poetry install
   ```

3. Скопировать `.env.template` в `.env` и заполнить:
   ```bash
   cp .env.template .env
   ```

4. Применить миграции:
   ```bash
   poetry run python manage.py migrate
   ```

5. Запустить сервер:
   ```bash
   poetry run python manage.py runserver
   ```

## Переменные окружения

| Переменная | Описание |
|---|---|
| `SECRET_KEY` | Секретный ключ Django |
| `DEBUG` | Режим отладки (True/False) |
| `CORS_ALLOWED_ORIGINS` | Список доменов через запятую |
| `TG_API_KEY` | Токен Telegram-бота |

## Эндпоинты

| Метод | URL | Описание |
|---|---|---|
| POST | `/users/register/` | Регистрация |
| POST | `/users/token/` | Получение JWT |
| POST | `/users/token/refresh/` | Обновление JWT |
| GET | `/habits/` | Список привычек (свои + публичные), пагинация по 5 |
| POST | `/habits/` | Создание привычки |
| GET | `/habits/{id}/` | Детали привычки |
| PUT/PATCH | `/habits/{id}/` | Редактирование (только свои) |
| DELETE | `/habits/{id}/` | Удаление (только свои) |
| GET | `/api/docs/` | Swagger UI |
| GET | `/api/schema/` | OpenAPI-схема |

## Celery и напоминания

Запуск воркера и планировщика:

```bash
poetry run celery -A config worker -l info
poetry run celery -A config beat -l info
```

Задача `send_habit_reminders` запускается раз в минуту и отправляет в Telegram напоминания о привычках, время которых совпадает с текущим.

## Тесты

```bash
poetry run coverage run manage.py test
poetry run coverage report
```

## Документация API

После запуска сервера доступна по адресу `/api/docs/`.
```
