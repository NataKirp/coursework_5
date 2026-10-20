# Habit Tracker API (Coursework 5)

Бэкенд-часть SPA-приложения для трекинга полезных привычек (по мотивам книги «Атомные привычки»). Проект полностью 
контейнеризирован, настроен CI/CD пайплайн с автоматическим деплоем на удаленный сервер.

## 🛠 Технологический стек
- **Python 3.12**, **Django 5.2**, **Django REST Framework**
- **PostgreSQL 16** (база данных)
- **Redis 7** (брокер сообщений и кэш)
- **Celery & Celery Beat** (фоновые задачи и планировщик)
- **Nginx** (reverse proxy и раздача статики)
- **Docker & Docker Compose**
- **GitHub Actions** (CI/CD)
- **Poetry** (управление зависимостями)

## 🚀 Запуск проекта локально

Для запуска проекта вам понадобятся установленные **Docker Desktop** и **Poetry**.

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/NataKirp/coursework_5.git
   cd coursework_5
   ```

2. **Настройте переменные окружения:**
   Скопируйте шаблон `.env.template` в `.env` и заполните своими данными:
   ```bash
   cp .env.template .env
   ```
   *Убедитесь, что в `.env` заданы `SECRET_KEY`, пароли для `POSTGRES`, а также `TG_API_KEY` для работы Telegram-бота.*

3. **Запустите проект одной командой:**
   ```bash
   docker compose up -d --build
   ```
   Эта команда соберет образы, поднимет все 6 сервисов (web, db, redis, celery, celery-beat, nginx) 
   и запустит их в фоне.

4. **Примените миграции и соберите статику:**
   ```bash
   docker compose exec web python manage.py migrate
   ```

5. **Проверьте работу:**
   Перейдите в браузере по адресу: **http://localhost/api/docs/** — откроется Swagger UI с документацией API.

## 🔄 CI/CD и Деплой на сервер

В проекте настроен пайплайн **GitHub Actions** (`.github/workflows/deploy.yml`), который состоит из четырех этапов:
1. **Lint** — проверка кода линтером `flake8`.
2. **Test** — запуск юнит-тестов Django (на SQLite для скорости).
3. **Build** — проверка успешной сборки Docker-образа.
4. **Deploy** — автоматический деплой на удаленный сервер (срабатывает только при пуше в ветку `main`).

### Настройка сервера
На сервере (Ubuntu) должны быть установлены Docker и Docker Compose. 
Проект разворачивается в директории `/var/www/habit_tracker`.

1. Клонируйте репозиторий на сервер (ветку `main`):
   ```bash
   cd /var/www/habit_tracker
   git clone -b main https://github.com/NataKirp/coursework_5.git .
   ```
2. Создайте файл `.env` прямо на сервере и заполните его боевыми настройками (обязательно установите `DEBUG=False`). 
   Ограничьте права доступа:
   ```bash
   chmod 600 .env
   ```

### Настройка GitHub Secrets
Для работы авто-деплоя в настройках репозитория (Settings -> Secrets and variables -> Actions) добавлены следующие 
секреты:
- `SERVER_IP` — IP-адрес сервера (например, `45.132.177.136`).
- `SSH_USER` — имя пользователя для SSH (например, `user1`).
- `SSH_KEY` — приватный SSH-ключ для доступа к серверу.
- `DEPLOY_DIR` — путь до папки с проектом на сервере (`/var/www/habit_tracker`).

### Как происходит деплой
При пуше в ветку `main` GitHub Actions заходит на сервер по SSH, делает `git reset --hard origin/main`, 
пересобирает контейнеры (`docker compose up -d --build`), применяет миграции, собирает статику и перезапускает Celery.

## 📡 Основные эндпоинты API

| Метод | URL | Описание |
|---|---|---|
| POST | `/users/register/` | Регистрация пользователя |
| POST | `/users/token/` | Получение JWT (авторизация) |
| POST | `/users/token/refresh/` | Обновление JWT |
| GET | `/habits/` | Список привычек (свои + публичные), пагинация по 5 |
| POST | `/habits/` | Создание привычки |
| GET | `/habits/{id}/` | Просмотр привычки |
| PUT/PATCH | `/habits/{id}/` | Редактирование (только свои) |
| DELETE | `/habits/{id}/` | Удаление (только свои) |
| GET | `/api/docs/` | Swagger UI (документация) |
| GET | `/api/schema/` | OpenAPI схема |

## 🧪 Тестирование

Запуск тестов и проверка покрытия:
```bash
poetry run coverage run manage.py test
poetry run coverage report
```
