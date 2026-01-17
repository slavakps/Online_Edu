Online Education Service
Сервис онлайн-образования с REST API.

Функционал:

- авторизованные пользователи работают с курсами и уроками через API
- JWT-аутентификация (SimpleJWT)
- доступ к данным ограничен правами пользователя
- реализованы подписки на курсы
- фоновые задачи выполняются через Celery
- Redis используется как брокер сообщений Celery
- API документация доступна через Swagger (drf-yasg)

Стек:

- Django, DRF
- PostgreSQL
- Celery + Redis
- Swagger (drf-yasg)
- GitHub Actions (tests + deploy)

Структура проекта

- core/ — настройки проекта Django (settings/urls/wsgi), celery config
- users/ — приложение пользователей (AUTH_USER_MODEL)
- materials/ — курсы/уроки/подписки, celery tasks
- .github/workflows/ — GitHub Actions workflow
- docker-compose.yml — локальный запуск Postgres + Redis + backend + celery
- .env.example — шаблон переменных окружения

Переменные окружения

Создай файл .env в корне проекта (можно скопировать из .env.example).

Переменные:

- SECRET_KEY
- DEBUG
- ALLOWED_HOSTS
- DB_NAME
- DB_USER
- DB_PASSWORD
- DB_HOST
- DB_PORT
- REDIS_HOST
- REDIS_PORT
- STRIPE_PUBLISHABLE_KEY
- STRIPE_SECRET_KEY
- EMAIL_HOST_USER
- EMAIL_HOST_PASSWORD
