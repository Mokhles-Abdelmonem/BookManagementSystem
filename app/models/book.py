from app import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    isbn = db.Column(db.String(13), unique=True, nullable=True)
    published_date = db.Column(db.String(10), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    cover = db.Column(db.String(200))
    language = db.Column(db.String(2), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'published_date': self.published_date,
            'pages': self.pages,
            'cover': self.cover,
            'language': self.language
        }

    def __repr__(self):
        return f'<Book "{self.title}">'
