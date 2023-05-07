from marshmallow import Schema, fields, validates, ValidationError, post_load
from flasgger import Schema, fields
from models import Book, Author


class AuthorSchema(Schema):
    id = fields.Integer(dump_only=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    middle_name = fields.String()

    @post_load
    def create_author(self, data: dict, *args, **kwargs) -> Author:
        return Author(**data)


class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author_id = fields.Integer(load_only=True, required=True)

    @post_load
    def create_book(self, data: dict, *args, **kwargs) -> Book:
        return Book(**data)
