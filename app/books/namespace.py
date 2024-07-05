import copy
from flask_restx import fields, Namespace


api = Namespace('book', description='Books related operations')

book_schema_no_id = api.model('Book', {
    'title': fields.String(required=True, description='The book title'),
    'author': fields.String(required=True, description='The book author'),
    'published_date': fields.String(required=True, description='The book published_date'),
    'pages': fields.Integer(required=True, description='The book pages'),
    'cover': fields.String(required=True, description='The book cover'),
    'language': fields.String(required=True, description='The book language'),
})

