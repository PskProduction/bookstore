# Bookstore API

Это простое API для книжного магазина, написанное с использованием Flask и Flask-RESTful. Он позволяет управлять книгами
и авторами, в том числе добавлять, обновлять и удалять записи.

## Запуск проекта

1. Установите Postgres на свой компьютер, используя инструкции, доступные на официальном
   сайте [Postgres](https://www.postgresql.org).


2. Создайте базу данных для проекта. Для этого можно использовать команду:

   ```sql
    CREATE DATABASE mydatabase;
   ```

3. Создайте пользователя для базы данных и назначьте ему необходимые права доступа. Для этого можно использовать
   команду:

   ```sql
   CREATE USER myuser WITH PASSWORD 'mypassword';
   ```  

   ```sql
   GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;
   ```

4. Создайте файл .env в корневой директории проекта и добавьте в него следующие настройки базы данных:

   `DATABASE_URL=postgresql://myuser:mypassword@localhost:5432/mydatabase`


5. Клонируйте репозиторий на свой компьютер:  
   `git clone https://github.com/PskProduction/bookstore-api.git`


6. Перейдите в директорию проекта:  
   `cd <название_репозитория>`


7. Установите зависимости:  
   `pip install -r requirements.txt`


8. Запустите сервер:  
   `python routes.py`

**API будет доступно по адресу http://localhost:5000**

## Маршруты:

- **GET /api/books**: получить список всех книг


- **POST /api/books**: добавить новую книгу 


- **GET /api/books/{book_id}**: получить информацию о книге по ее идентификатору


- **PUT /api/books/{book_id}**: обновить информацию о книге по ее идентификатору


- **DELETE /api/books/{book_id}**: удалить книгу из магазина по ее идентификатору


- **POST /api/authors**: добавить нового автора 


- **GET /api/authors/{int:author_id}**: получить cписок книг, которые написал автор


- **DELETE /api/authors/{int:author_id}**: удалить автора по его идентификатору

## Документация
**Вы можете получить документацию к API в формате Swagger, по адресу:  http://localhost:5000/apidocs.**

