# Сервис для хранения секретных данных

JSON API сервис позволяет шифровать и хранить секретные данные с ограниченным временем жизни. 

## Используемый стек

- [FastAPI](https://fastapi.tiangolo.com/) современный, быстрый (высокопроизводительный) веб-фреймворк для создания API.
- [Uvicorn](https://www.uvicorn.org/) реализация веб-сервера ASGI для Python.
- [Pytest](https://docs.pytest.org/en/7.4.x/contents.html) полнофункциональный инструмент тестирования на Python
- [Docker](https://docs.docker.com/get-started/overview/) открытая платформа для разработки, доставки и запуска приложений.
- [Docker compose](https://docs.docker.com/compose/) инструмент для определения и запуска многоконтейнерных приложений Docker. 


## Установка 
Для проведения установки необходимо, чтобы пользователь от которого выполняются действия находился в группе `docker`
### Порядок действий:
1. Поставьте Docker по [инструкции с сайта Docker](https://docs.docker.com/engine/install/ubuntu/)
2. Склонируйте репозиторий на сервер, например, в директорию: `/home/<user>/`:

    ```bash
    git clone https://github.com/AndMartyan/secret_marks.git
    ```


## Запуск с помощью Docker Compose

1. Склонируйте репозиторий:

    ```bash
    git clone https://github.com/AndMartyan/secret_marks.git
    ```

2. Перейдите в каталог с сервисом:

    ```bash
    cd your-service
    ```

3. Создайте файл `.env` и укажите в нем необходимые переменные окружения (например, `DB_USER`, `DB_PASS`, `DB_NAME`):

    ```env
    DB_USER=myuser
    DB_PASS=mypassword
    DB_NAME=mydatabase
    ```

4. Запустите сервис с помощью Docker Compose:

    ```bash
    docker-compose up -d
    ```

5. Сервис будет доступен по адресу `http://localhost:8000`.

## Остановка сервиса

Для остановки сервиса выполните следующую команду:

```bash
docker-compose down
