from flask import Flask
from config import Config
from app.extensions import db, bcrypt, jwt
from flask_restx import Api


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    authorizations = {
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    }

    api = Api(
        title='Book Management System',
        version='1.0',
        description='Flask-based web application designed to manage books, user accounts, '
                    'authentication and interactions such as wishlist and liked books,'
                    ' using pydantic as a validation tool for equest and response formats',
        authorizations=authorizations,
        security='Bearer Auth'
    )
    from app.auth.routes import api as auth_ns
    api.add_namespace(auth_ns)

    from app.users.routes import api as users_ns
    api.add_namespace(users_ns)

    from app.books.routes import api as books_ns
    api.add_namespace(books_ns)

    api.init_app(app)

    return app
