# Вступительное задание в Летнюю ШБР Яндекса 2022

Проект представляет собой API магазина, реализующий CRUD функционал для товаров + получение особых данных (скидок,
истории изменения). Задание выполнено полностью, реализованы базовые и дополнительные задачи.

Технологии: Python, FastApi, SQLAlchemy, PostgreSQL

По умолчанию проект запускается на 0.0.0.0:80. Доступна авто-генерируемая интерактивная документация к маршрутам, чтобы
открыть, перейдите на **/docs**. Имеются тесты.

## Установка и запуск

Клонируйте файлы проекта с помощью команды `git clone`. Дальнейшие шаги зависят от того, будете ли вы использовать
Docker для запуска или нет

### Без Docker

1. Установите зависимости

```console
pip install -r requirements.txt
```

2. В .env файле укажите ссылку для подключения к базе данных в параметр POSTGRES_URL_DOCKER. Установите
   PostgreSQL (https://www.postgresql.org/) и запустите его сервер, если раннее не сделали это.
3. Запустите main.py

```console
python main.py
```

Готово! 😎 \
Апи будет доступно на 0.0.0.0:80.

### Используя Docker

В репозитории уже имеются готовые файлы (Dockerile и docker-compose.yml) для запуска приложения с помощью Docker. В
docker-compose.yml прописана конфигурация базы данных, при желании вы можете изменить её.

Для запуска используйте:

```console
docker-compose up
```

Готово! 😎 \
Апи будет доступно на 0.0.0.0:80.

## Тестирование

В проекте имеются тесты, которые покрывают:

- валидацию данных при запросе
- работу маршрутов, логики
- особые случаи

### Запуск тестов

1. Установите pytest

```console
pip install pytest
```

2. Запустите, используя команду в корневой директории проекта

```console
pytest
```

И вам отобразится результат работы тестов