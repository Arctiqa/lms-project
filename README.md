# LMS Platform — REST API

Pet-проект: backend-платформа для онлайн-обучения с курсами, уроками, подписками, оплатой через Stripe и фоновыми задачами на Celery.

## Стек

- Python 3.11+, Django 4.2
- Django REST Framework + SimpleJWT (авторизация)
- PostgreSQL (psycopg2)
- Celery + Redis + django-celery-beat (фон и периодические задачи)
- Stripe (приём платежей)
- drf-yasg (Swagger/ReDoc)
- django-filter, django-cors-headers
- Pillow (изображения), python-dotenv (конфиг)

## Возможности

- Кастомная модель User (вход по email, аватар, телефон, город)
- JWT-аутентификация (/users/token/, /users/token/refresh/)
- CRUD курсов и уроков с разграничением прав: IsOwner — владелец объекта, IsModerator — модератор (группа moderator)
- Пагинация списков (10 на страницу)
- Валидация ссылок в уроках (только YouTube)
- Подписка на курс (POST /users/subscription/ — toggle)
- Оплата через Stripe: создание продукта, цены, checkout-сессии; сохранение session_id и link в Payment
- Celery-задачи: send_email_update_course — письмо подписчикам при обновлении курса; check_user_activity — блокировка пользователей, не заходивших 30 дней
- Swagger / ReDoc документация

## Установка

git clone <repo-url>
cd <project>
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

### Переменные окружения (.env)

SECRET_KEY=your-secret-key
POSTGRES_DB=lms
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
EMAIL_HOST_USER=you@yandex.ru
EMAIL_HOST_PASSWORD=app-password
STRIPE_API_KEY=sk_test_...
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

### Миграции и запуск

python manage.py migrate
python manage.py csu        # создать суперпользователя
python manage.py runserver

### Celery (worker + beat)

celery -A config worker -l info
celery -A config beat -l info

## Основные эндпоинты

| Метод | URL | Описание |
|-------|-----|----------|
| POST | /users/create/ | Регистрация |
| POST | /users/token/ | Получить JWT |
| POST | /users/token/refresh/ | Обновить JWT |
| GET/PUT/DELETE | /users/<pk>/, /users/update/<pk>/, /users/delete/<pk>/ | Профиль |
| GET | /users/payments/ | Платежи (фильтры, сортировка) |
| POST | /users/subscription/ | Toggle подписки |
| POST | /users/payment/ | Оплата через Stripe |
| CRUD | /courses/ | Курсы (ViewSet) |
| CRUD | /lesson/... | Уроки |

## Документация

- Swagger: http://127.0.0.1:8000/swagger/
- ReDoc: http://127.0.0.1:8000/redoc/

## Тесты

python manage.py test

Покрыты: создание/список/обновление/удаление уроков, toggle подписки.

## Структура

config/       — настройки, celery, urls
users/        — User, Payment, Subscription, JWT, Stripe
lms/          — Course, Lesson, права, валидаторы, задачи
