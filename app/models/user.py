from app import db
from datetime import datetime

# Association table for wishlist
wishlist_table = db.Table(
    'wishlist',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True)
)

# Association table for liked books
liked_books_table = db.Table(
    'liked_books',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True)
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    first_name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(30), nullable=True)
    profile_picture = db.Column(db.String(200), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    birthdate = db.Column(db.Date, nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    refresh_token_jti = db.Column(db.String(36), nullable=True)
    wishlist = db.relationship('Book', secondary=wishlist_table, backref='wishlisted_by')
    liked_books = db.relationship('Book', secondary=liked_books_table, backref='liked_by')

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'profile_picture': self.profile_picture,
            'address': self.address,
            'birthdate': self.birthdate,
            'is_active': self.is_active,
            'is_admin': self.is_admin,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'last_login': self.last_login,
            'wishlist': [book.to_dict() for book in self.wishlist],
            'liked_books': [book.to_dict() for book in self.liked_books]
        }

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
