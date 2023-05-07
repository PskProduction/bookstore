import psycopg2
from dataclasses import dataclass
from typing import Optional, Union, List, Dict

DATA = [
    {'id': 1, 'title': 'A Byte of Python', 'author': {'first_name': 'Swaroop C. H.', 'last_name': 'C', 'middle_name': 'H'}},
    {'id': 2, 'title': 'Moby-Dick; or, The Whale', 'author': {'first_name': 'Herman ', 'last_name': 'Melville'}},
    {'id': 3, 'title': 'War and Peace', 'author': {'first_name': 'Leo', 'last_name': 'Tolstoy'}},

]

DATABASE_URL = 'DATABASE_URL=postgresql://myuser:mypassword@localhost:5432/mydatabase'
BOOKS_TABLE_NAME = 'books'
AUTHORS_TABLE_NAME = 'authors'


@dataclass
class Author:
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    id: Optional[int] = None

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)


@dataclass
class Book:
    title: str
    author_id: int
    id: Optional[int] = None

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)


def init_db(initial_records: List[Dict]) -> None:
    with psycopg2.connect(DATABASE_URL) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
                    SELECT tablename FROM pg_tables WHERE schemaname='public' AND tablename='{AUTHORS_TABLE_NAME}';
                    """
        )
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(
                f"""
                        CREATE TABLE IF NOT EXISTS "{AUTHORS_TABLE_NAME}"(
                            id SERIAL PRIMARY KEY, 
                            first_name TEXT,
                            last_name TEXT,
                            middle_name TEXT
                        );
                        """
            )

        cursor.execute(
            f"""
            SELECT tablename FROM pg_tables WHERE schemaname='public' AND tablename='{BOOKS_TABLE_NAME}';
            """
        )
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS "{BOOKS_TABLE_NAME}"(
                    id SERIAL PRIMARY KEY,
                    title TEXT,
                    author_id INTEGER REFERENCES "{AUTHORS_TABLE_NAME}" (id) ON DELETE CASCADE
                );
                """
            )

            cursor.executemany(
                f"""
                INSERT INTO "{AUTHORS_TABLE_NAME}"
                (first_name, last_name, middle_name) VALUES (%s, %s, %s)
                """,
                [
                    (item['author']['first_name'], item['author']['last_name'], item['author'].get('middle_name'))
                    for item in initial_records
                ]
            )

            cursor.executemany(
                f"""
                INSERT INTO "{BOOKS_TABLE_NAME}"
                (title, author_id) VALUES (%s, %s)

                """,
                [
                    (item['title'], item['id']) for item in initial_records
                ]
            )


def _get_book_obj_from_row(row: tuple) -> Book:
    return Book(id=row[0], title=row[1], author_id=row[2])


def get_all_books() -> list[Book]:
    with psycopg2.connect(DATABASE_URL) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM "{BOOKS_TABLE_NAME}"')
        all_books = cursor.fetchall()
        return [_get_book_obj_from_row(row) for row in all_books]


def add_book(book: Book) -> Book:
    with psycopg2.connect(DATABASE_URL) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO "{BOOKS_TABLE_NAME}" 
            (title, author_id) VALUES (%s, %s) 
            RETURNING id
            """,
            (book.title, book.author_id)
        )
        book.id = cursor.fetchone()[0]
        return book


def get_book_by_id(book_id: int) -> Optional[Book]:
    with psycopg2.connect(DATABASE_URL) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM "{BOOKS_TABLE_NAME}" WHERE id = %s
            """,
            (book_id,)
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


def update_book_by_id(book: Book) -> None:
    with psycopg2.connect(DATABASE_URL) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            UPDATE "{BOOKS_TABLE_NAME}"
            SET title = %s, author_id = %s
            WHERE id = %s
            """,
            (book.title, book.author_id, book.id)
        )
        conn.commit()


def delete_book_by_id(book_id: int) -> None:
    with psycopg2.connect(DATABASE_URL) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            DELETE FROM "{BOOKS_TABLE_NAME}"
            WHERE id = %s
            """,
            (book_id,)
        )
        conn.commit()


def get_book_by_title(book_title: str) -> Optional[Book]:
    with psycopg2.connect(DATABASE_URL) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT *
            FROM "{BOOKS_TABLE_NAME}"
            WHERE title = %s
            """,
            (book_title,)
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


def _get_author_obj_from_row(row: tuple) -> Author:
    return Author(id=row[0], first_name=row[1], last_name=row[2], middle_name=row[3])


def get_all_authors() -> list[Author]:
    with psycopg2.connect(DATABASE_URL) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM "{AUTHORS_TABLE_NAME}"')
        all_authors = cursor.fetchall()
        return [_get_author_obj_from_row(row) for row in all_authors]


def get_author_by_id(author_id: int) -> Optional[Author]:
    with psycopg2.connect(DATABASE_URL) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * FROM "{AUTHORS_TABLE_NAME}" WHERE id = %s
            """,
            (author_id,)
        )
        author = cursor.fetchone()
        if author is None:
            return None
        return _get_author_obj_from_row(author)


def add_author(author: Author) -> Author:
    with psycopg2.connect(DATABASE_URL) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            INSERT INTO "{AUTHORS_TABLE_NAME}"
            (first_name, last_name, middle_name) VALUES (%s, %s, %s)
            RETURNING id
            """,
            (author.first_name, author.last_name, author.middle_name or None)
        )
        author.id = cursor.fetchone()[0]
        return author


def get_books_author_by_id(author_id: int) -> List[Book]:
    with psycopg2.connect(DATABASE_URL) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * 
            FROM "{BOOKS_TABLE_NAME}"
            WHERE author_id = %s
            """,
            (author_id,)
        )
        books = cursor.fetchall()
        return [_get_book_obj_from_row(book) for book in books]


def delete_author_by_id(author_id: int) -> None:
    with psycopg2.connect(DATABASE_URL) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            DELETE
            FROM {AUTHORS_TABLE_NAME}
            WHERE id = %s
            """,
            (author_id,)
        )
        conn.commit()

