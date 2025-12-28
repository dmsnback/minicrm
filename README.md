<a name="Начало"></a>

# miniCRM

API мини CRM приложеение

[![miniCRM Lint](https://img.shields.io/github/actions/workflow/status/dmsnback/minicrm/main.yml?branch=main&style=flat-square&label=miniCRM%20Lint)](https://github.com/dmsnback/minicrm/actions/workflows/main.yml)
[![miniCRM Docker Dev](https://img.shields.io/github/actions/workflow/status/dmsnback/minicrm/main.yml?branch=dev&style=flat-square&label=miniCRM%20Docker%20Dev)](https://github.com/dmsnback/minicrm/actions/workflows/main.yml)
[![miniCRM Docker Prod](https://img.shields.io/github/actions/workflow/status/dmsnback/minicrm/main.yml?branch=main&style=flat-square&label=miniCRM%20Docker%20Prod)](https://github.com/dmsnback/minicrm/actions/workflows/main.yml)


- [Описание](#Описание)
- [Технологии](#Технологии)
- [Таблица эндпоинтов](#Таблица)
- [Шаблон заполнения .env-файла](#Шаблон)
- [Запуск проекта на локальной машине](#Запуск)
- [Автор](#Автор)

<a name="Описание"></a>
### Описание

MiniCRM — это backend-сервис для управления клиентами, сделками и комментариями, реализованный на FastAPI с асинхронной работой через PostgreSQL.

Проект ориентирован на практическую разработку API с авторизацией, ролями пользователей и правами доступа.

REST API для управления:

- Клиентами (CRUD)
- Сделками (CRUD, статусы, фильтрация по менеджерам)
- Комментариями к сделкам
- Пользователями с ролями (admin / manager)
- Авторизацией через JWT

Приложение написано с использованием **асинхронного FastAPI**, **SQLAlchemy**, **PostgreSQL** и **FastAPI Users**.

```python
Проект адаптирован для использования PostgreSQL и развёртывания в контейнерах Docker.
```

> [Вернуться в начало](#Начало)
<a name="Технологии"></a>

### Технологии


[![Python](https://img.shields.io/badge/Python-1000?style=for-the-badge&logo=python&logoColor=ffffff&labelColor=000000&color=000000)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-1000?style=for-the-badge&logo=fastapi&logoColor=ffffff&labelColor=000000&color=000000)](https://fastapi.tiangolo.com)
[![FastAPI Users](https://img.shields.io/badge/FastAPI_Users-1000?style=for-the-badge&logoColor=ffffff&labelColor=000000&color=000000)](https://fastapi-users.github.io/fastapi-users/latest/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1000?style=for-the-badge&logo=sqlalchemy&logoColor=ffffff&labelColor=000000&color=000000)](https://www.sqlalchemy.org)
[![Pydantic](https://img.shields.io/badge/Pydantic_V2-1000?style=for-the-badge&logo=Pydantic&logoColor=ffffff&labelColor=000000&color=000000)](https://docs.pydantic.dev/latest/)
[![Docker](https://img.shields.io/badge/Docker-1000?style=for-the-badge&logo=docker&logoColor=ffffff&labelColor=000000&color=000000)](https://www.docker.com)
[![Postgres](https://img.shields.io/badge/Postgres-1000?style=for-the-badge&logo=postgresql&logoColor=ffffff&labelColor=000000&color=000000)](https://www.postgresql.org)
[![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=ffffff&labelColor=000000&color=000000)](https://github.com/features/actions)

> [Вернуться в начало](#Начало)
<a name="Таблица"></a>

### Таблица эндпоинтов

**Авторизация**

|Метод|URL|Описание|Доступ|
|:-:|:-:|:-:|:-:|
|POST|/auth/register|Регистрация новых менеджеров|Админ|
|POST|/auth/jwt/login|получение JWT токена|Админ<br> Менеджер|

**Пользователи**

|Метод|URL|Описание|Доступ|
|:-:|:-:|:-:|:-:|
|GET|/users/all|Список всеех менеджеров|Админ|
|GET|/users/{user_id}/clients|Получение списка клиентов менеджра по id|Админ|
|GET|/users/me|Получение текущего юзера|Админ<br> Менеджер|
|PATCH|/users/{id}|Редактирование юзера|Админ|
|DELETE|/users/{id}|Удаление юзера|Админ|

**Клиенты**

|Метод|URL|Описание|Доступ|
|:-:|:-:|:-:|:-:|
|GET|/clients/all|Список всех клиентов<br>(Админ видит всех, менеджер - своих)|Админ<br> Менеджер|
|GET|/clients/{clients_id}|Получение клиента по id|Админ<br> Менеджер|
|PATCH|/clients/{clients_id}|Редактирование клиента|Админ<br> Менеджер|
|DELETE|/clients/{clients_id}|Удаление клиентв|Админ|
|POST|/clients|Добавление нового клиента|Админ<br> Менеджер|

**Сделки**

|Метод|URL|Описание|Доступ|
|:-:|:-:|:-:|:-:|
|GET|/deals/all|Список всех сделок<br>(Админ видит вс своих)|Админ<br> Менеджер|
|GET|/deals/{deals_id}|Получение сделки по id|Админ<br> Менеджер|
|PATCH|/deals/{deals_id}|Редактирование сделки|Админ<br> Менеджер|
|DELETE|/deals/{deals_id}|Удаление сделки|Админ|
|POST|/deals|Добавление новой сделки|Админ<br> Менеджер|

**Комментарии**

|Метод|URL|Описание|Доступ|
|:-:|:-:|:-:|:-:|
|GET|/comments/{deal_id}/comments|Получить все комментарии сделки|Админ<br> Менеджер|
|POST|/comments/{deal_id}/comments|Добавление комментария к сделке|Админ<br> Менеджер|
|PATCH|/comments/{deal_id}/comments/{comment_id}|Редактирование комментария|Админ<br> Менеджер|
|DELETE|/comments/{deal_id}/comments/{comment_id}|Удаление комментария|Админ|

> [Вернуться в начало](#Начало)

<a name="Шаблон"></a>

### Шаблон заполнения .env-файла

> `env.example` с дефолтнными значениями расположен в корневой папке

```python
POSTGRES_DB = minicrmdb # Имя базы дданнных
POSTGRES_USER = postgres # Имя юзера PostgreSQL
POSTGRES_PASSWORD = yourpassword # Пароль юзера PostgreSQL
DATABASE_URL = postgresql+asyncpg://postgres:yourpassword@db:5432/minicrmdb  # Указываем адрес БД
DEBUG = False # Включеение/Выключение режима отладки
APP_TITLE = МиниCRM приложение # Название приложения
SECRET = SUPERSECRETKEY # Секретный ключ для подписания JWT токенов
FIRST_SUPERUSER_USERNAME = superadmin # Указываеем usernsme для суперюзера
FIRST_SUPERUSER_EMAIL = superadmin@mail.com # Указываеем почту для суперюзера
FIRST_SUPERUSER_PASSWORD = superadmin # Указываеем пароль для суперюзера
FIRST_SUPERUSER_ROLE = admin # Указываеем роль для суперюзера
```

> [Вернуться в начало](#Начало)

<a name="Запуск"></a>

### Запуск проекта на локальной машине

- Склонируйте репозиторий

```python
git clone git@github.com:dmsnback/minicrm.git
```

- Запускаем Docker контейнер

```python
docker-compose up -d --build
```

- Выполняем миграции

```python
docker-compose exec backend alembic upgrade head   
```

- Создаём суперюзера

```python
docker-compose exec backend python create_superuser.py
```

> __Документация к API будет доступна по адресу:__

[http://localhost:8000/docs/](http://localhost:8000/docs/)

> [Вернуться в начало](#Начало)

<a name="Авторы"></a>

### Автор

- [Титенков Дмитрий](https://github.com/dmsnback)

> [Вернуться в начало](#Начало)
