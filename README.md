# Проект YaMDb
## Описание проекта
- Проект YaMDb собирает отзывы пользователей на произведения.
- Произведения делятся на категории: Музыка, Фильмы, Книги.
- Список категорий может быть расширен администратором.
- Произведению может быть присвоен жанр из списка предустановленных. Новые жанры может создавать только администратор.
- Пользователи могут ставить произведениям оценки что в дальнейшем повлияет на усреднённый рейтинг произведения.

## Для реализации проекта используются:
- Django 2.2.16
- Django REST Framework 3.12.4

# Установка проекта
## Клонировать репозиторий и перейти в него в командной строке:
- git clone https://github.com/Denis-Guselnikov/api_yamdb
- cd api_yamdb/
## Cоздание виртуального окружения и его активация:
- python -m venv venv
- source venv/Scripts/activate
## Установка зависимостей из requirements.txt:
- pip install -r requirements.txt
## Выполнение миграций:
- python manage.py migrate
## Запуск проекта:
- cd yatube_api/
- python3 manage.py runserver

## Документация к API
http://127.0.0.1:8000/redoc/

## Над проектом работали
- Николай Морозов: отзывы, комментарии
- Денис Гусельников: категории, жанры, произведения
- Денис Попов: пользователи, регистрация и аутентификация
