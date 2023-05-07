from typing import Union

from flasgger import Swagger
from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow import ValidationError
from werkzeug.serving import WSGIRequestHandler

from models import (
    DATA,
    get_all_books,
    init_db,
    add_book,
    get_book_by_id,
    update_book_by_id,
    delete_book_by_id,
    add_author,
    delete_author_by_id, get_author_by_id, get_books_author_by_id,
)
from schemas import BookSchema, AuthorSchema

app = Flask(__name__)
api = Api(app)


class BookList(Resource):
    def get(self) -> tuple[list[dict], int]:

        schema = BookSchema()
        return schema.dump(get_all_books(), many=True), 200

    def post(self) -> tuple[dict, int]:
        data = request.json
        schema = BookSchema()
        try:
            book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        author = get_author_by_id(book.author_id)
        if author is None:
            return {"message": "Author not found"}, 404

        book = add_book(book)
        return schema.dump(book), 201


class BookItem(Resource):
    def get(self, book_id: int) -> Union[dict, tuple[dict, int]]:
        book = get_book_by_id(book_id)
        if book is None:
            return {'message': 'Book not found'}, 400
        schema = BookSchema()
        return schema.dump(book), 200

    def put(self, book_id) -> Union[dict, tuple[dict, int]]:
        data = request.json
        schema = BookSchema()

        book = get_book_by_id(book_id)
        if book is None:
            return {'message': 'Book not found'}, 400
        try:
            book_data = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        book.title = book_data.title
        book.author_id = book_data.author_id

        update_book_by_id(book)

        return schema.dump(book), 200

    def delete(self, book_id: int) -> tuple[dict, int]:
        book = get_book_by_id(book_id)
        if book is None:
            return {'message': 'Book not found'}, 400

        delete_book_by_id(book_id)

        return {'message': 'Book delete successfully'}, 200


class AuthorList(Resource):
    def post(self) -> tuple[dict, int]:
        data = request.json
        schema = AuthorSchema()
        try:
            author = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        author = add_author(author)
        return schema.dump(author), 201


class AuthorItem(Resource):
    def get(self, author_id: int) -> Union[dict, tuple[dict, int]]:
        author = get_author_by_id(author_id)
        if author is None:
            return {'message': 'Author not found'}, 404

        books = get_books_author_by_id(author_id)
        schema = AuthorSchema()
        author_data = schema.dump(author)
        author_data['books'] = [book.__dict__ for book in books]

        return author_data, 200

    def delete(self, author_id: int) -> tuple[dict, int]:
        author = get_author_by_id(author_id)
        if author is None:
            return {'message': 'Author not found'}, 404
        delete_author_by_id(author_id)
        return {'message': 'Author deleted successfully'}, 204


swagger_authors = Swagger(app, template_file='docs/bookstore.yml')

api.add_resource(BookList, '/api/books')
api.add_resource(BookItem, '/api/books/<int:book_id>')
api.add_resource(AuthorList, '/api/authors')
api.add_resource(AuthorItem, '/api/authors/<int:author_id>')

if __name__ == '__main__':
    init_db(initial_records=DATA)
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(debug=True)
