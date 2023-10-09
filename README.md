# Сервис для хранения секретных данных

JSON API сервис, который позволяет шифровать и хранить секретные данные с ограниченным временем жизни. 

## Используемый стек

- [FastAPI](https://fastapi.tiangolo.com/) современный, быстрый (высокопроизводительный) веб-фреймворк для создания API.
- [PostgreSQL](https://www.postgresql.org) — свободная объектно-реляционная система управления базами данных.
- [Uvicorn](https://www.uvicorn.org/) реализация веб-сервера ASGI для Python.
- [Pytest](https://docs.pytest.org/en/7.4.x/contents.html) полнофункциональный инструмент тестирования на Python
- [Docker](https://docs.docker.com/get-started/overview/) открытая платформа для разработки, доставки и запуска приложений.
- [Docker compose](https://docs.docker.com/compose/) инструмент для определения и запуска многоконтейнерных приложений Docker. 


## Установка 
ВНИМАНИЕ! Для проведения установки необходимо, чтобы пользователь от которого выполняются действия находился в группе `sudo`
### Порядок действий:
1. Установите Docker по [инструкции с сайта Docker](https://docs.docker.com/engine/install/ubuntu/)
2. Установите ”make”
    ```bash
    sudo apt install make
    ```
2. Склонируйте репозиторий на сервер, например, в директорию: `/home/<user>/`:

    ```bash
    sudo git clone https://github.com/AndMartyan/secret_marks.git
    ```
3. Перейдите в каталог с сервисом:

    ```bash
    cd secret_marks
    ```
4. При необходимости измените параметры в `Makefile` и `docker-compose.yml`
5. Отредактируйте файл `.env-non-dev`
   ```bash
   DB_HOST=db #хост продакшн-базы 
   DB_PORT=1221 #порт продакшн-базы 
   DB_NAME=postgres #название продакшн-базы 
   DB_USER=postgres #имя пользователя продакшн-базы 
   DB_PASS=postgres #пароль пользователя продакшн-базы 
   
   DB_HOST_TEST=db #хост тестовой базы 
   DB_PORT_TEST=1221 #порт тестовой базы 
   DB_NAME_TEST=postgres #название тестовой базы
   DB_USER_TEST=postgres #имя пользователя тестовой базы
   DB_PASS_TEST=postgres #пароль пользователя тестовой базы
   
   POSTGRES_DB=postgres
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   
   KEY_PATH =encryption_key.txt #путь к ключу шифрования
    ```
6. Выполните команду:

    ```bash
    sudo make container
    ```

7. Запустите сервис с помощью Docker Compose:

    ```bash
    sudo docker compose -p secret_marks \
                -f docker-compose.yml \
                up -d
    ```
8. Проверьте работоспособность сервиса в соответствии с настройками

## Остановка сервиса

Для остановки сервиса выполните следующую команду:

   ```bash
   sudo docker compose -p secret_marks  stop
   ```

## Работа сервиса
Сервис имеет два эндпоинта:

- `POST /generate` принимает секрет, кодовую фразу и период жизни секрета в минутах, возвращает secret_key по которому этот секрет можно получить.
  Пример отправки HTTP-запроса:
  ```python3
  import requests
  UVICORN_SCHEME = 'http://'
  UVICORN_HOST = '127.0.0.1'
  UVICORN_PORT = '8000'
  response = requests.post(url=UVICORN_SCHEME + UVICORN_HOST + ":" + UVICORN_PORT + '/generate/',
                         json={"secret": "string","passphrase": "string","lifetime_minutes": 0})
  ```
- `GET /secrets/{secret_key}` принимает на вход кодовую фразу и отдает секрет.
  Пример отправки HTTP-запроса:
  ```python3
  import requests
  UVICORN_SCHEME = 'http://'
  UVICORN_HOST = '127.0.0.1'
  UVICORN_PORT = '8000'
  secret_key = ''
  response = requests.get(url=UVICORN_SCHEME + UVICORN_HOST + ":" + UVICORN_PORT + f'/secrets/{secret_key}', json = {"passphrase": "string"}) 
  ```
Подробная документация доступна по эндпоинту : `GET <fastapi_sevice>/docs` 

## Тестирование
Выполните команду 
```python3
sudo docker exec secret_marks pytest tests/test_app.py
```


## Версия

23.10