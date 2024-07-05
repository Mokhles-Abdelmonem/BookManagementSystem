from flask import abort
from app.books.namespace import book_schema_no_id
from .schemas import BookSchemaIn, BookSchemaOut
from flask_restx import Resource, fields
from flask import request
from app import db
from app.middlewares import validate
from app.models.user import User
from app.models.book import Book
from app.books.namespace import api
from flask_jwt_extended import jwt_required, get_jwt_identity

@api.route('/')
class BookList(Resource):

    @validate(response_model=BookSchemaOut, is_list=True)
    @api.doc("get_books")
    def get(self):
        books = Book.query.all()
        return books

    @validate(request_model=BookSchemaIn, response_model=BookSchemaOut)
    @jwt_required()
    @api.doc("add_book")
    @api.expect(book_schema_no_id)
    def post(self):
        data = request.get_json()
        existing_book = Book.query.filter_by(title=data['title']).first()
        if existing_book:
            abort(400, 'Book already exists')

        book = Book(
            title=data['title'],
            author=data['author'],
            isbn=data.get('isbn'),  # Optional field
            published_date=data['published_date'],
            pages=data['pages'],
            cover=data.get('cover'),  # Optional field
            language=data['language']
        )
        db.session.add(book)
        db.session.commit()

        return book.to_dict(), 201


@api.route('/<int:pk>')
@api.param('pk', 'The book identifier')
class BookResource(Resource):

    @validate(response_model=BookSchemaOut)
    @api.doc("get_book")
    def get(self, pk):
        book = Book.query.get(pk)
        if not book:
            abort(404, 'Book not found')
        return book.to_dict()

    @validate(request_model=BookSchemaIn, response_model=BookSchemaOut)
    @jwt_required()
    @api.doc("update_book")
    @api.expect(book_schema_no_id)
    def put(self, pk):
        book = Book.query.get(pk)
        if not book:
            abort(404, 'Book not found')
        data = request.get_json()
        for key, value in data.items():
            if hasattr(book, key):
                setattr(book, key, value)
        db.session.commit()
        return book.to_dict()

    @validate()
    @jwt_required()
    @api.doc("delete_book")
    @api.response(204, 'Book deleted')
    def delete(self, pk):
        book = Book.query.get(pk)
        if not book:
            abort(404, 'Book not found')
        db.session.delete(book)
        db.session.commit()
        return {'message': 'Book deleted successfully'}, 204


@api.route('/wishlist')
class UserWishlist(Resource):
    @jwt_required()
    @api.doc("get_wishlist")
    @validate(response_model=BookSchemaOut)
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        return user.to_dict()['wishlist']

    @jwt_required()
    @api.expect(api.model('BookId', {'book_id': fields.Integer(required=True)}))
    @api.doc("add_to_wishlist")
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        data = request.get_json()
        book = Book.query.get(data['book_id'])

        if not book:
            return {'message': 'Book not found'}, 404

        if book in user.wishlist:
            return {'message': 'this book in your liked books '}, 409

        user.wishlist.append(book)
        db.session.commit()
        return {'message': 'Book added to wishlist'}

    @jwt_required()
    @api.expect(api.model('BookId', {'book_id': fields.Integer(required=True)}))
    @api.doc("remove_from_wishlist")
    def delete(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        data = request.get_json()
        book = Book.query.get(data['book_id'])

        if not book or not book in user.wishlist:
            return {'message': 'Book not found'}, 404

        user.wishlist.remove(book)
        db.session.commit()
        return {'message': 'Book removed from wishlist'}


@api.route('/liked_books')
class UserLikedBooks(Resource):
    @jwt_required()
    @api.doc("get_liked_books")
    @validate(response_model=BookSchemaOut)
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        return user.to_dict()['liked_books']

    @jwt_required()
    @api.expect(api.model('BookId', {'book_id': fields.Integer(required=True)}))
    @api.doc("add_to_liked_books")
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        data = request.get_json()
        book = Book.query.get(data['book_id'])

        if not book:
            return {'message': 'Book not found'}, 404
        if book in user.liked_books:
            return {'message': 'this book in your liked books '}, 409

        user.liked_books.append(book)
        db.session.commit()
        return {'message': 'Book added to liked books'}

    @jwt_required()
    @api.expect(api.model('BookId', {'book_id': fields.Integer(required=True)}))
    @api.doc("remove_from_liked_books")
    def delete(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        data = request.get_json()
        book = Book.query.get(data['book_id'])
        if not book or not book in user.liked_books:
            return {'message': 'Book not found'}, 404

        user.liked_books.remove(book)
        db.session.commit()
        return {'message': 'Book removed from liked books'}
