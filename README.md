# FastAPI & SQLAlchemy Project

## Описание

Этот проект использует FastAPI для создания веб-приложений с базой данных, 
подключенной через SQLAlchemy. Проект включает в себя основные функции, 
такие как маршруты, модели данных, а также CRUD-операции и обработку данных 
с помощью Pydantic. Он предоставляет API для работы с базой данных 
и демонстрирует, как интегрировать FastAPI с SQLAlchemy.

## Установка

### Требования

- Python 3.8+
- pip
- Virtualenv (рекомендуется для изоляции окружения)

### Шаги по установке

1. **Клонировать репозиторий:**

   ```bash
   git clone https://github.com/KVoff/SQLAlchemy_diplom.git
   
2. **Создайте и активируйте виртуальное окружение:**
На Windows:
    ```bash
    python -m venv venv
    venv\Scripts\activate
   
На Mac/Linux:

    python3 -m venv venv
    source venv/bin/activate

3. **Установите зависимости проекта:**
    ```bash
   pip install -r requirements.txt

4. **Настройте базу данных:**
В проекте используется SQLAlchemy для работы с базой данных.
Подключение к базе данных настраивается в файле database.py.

5. **После этого выполните миграции базы данных с помощью Alembic:**
    ```bash
   alembic revision --autogenerate -m "описание изменений"
   alembic upgrade head

6. **Запустите сервер разработки:**
    ```bash
   uvicorn main:app --reload
   
Сервер будет доступен по адресу: http://127.0.0.1:8000/

7. **Запуск тестов:**
    ```bash
   PYTHONPATH=$(pwd) pytest test/
   
данные о тестах сохраняются в папке test
test_logs.log
test_time.log

8. **Работа с API**

Для работы с API используйте встроенный 
http://127.0.0.1:8000/docs


