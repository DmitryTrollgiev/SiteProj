from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    fio = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='reader')
    posts = db.relationship('Post', backref='author', lazy=True)
    ex_books = db.relationship('ExtraditionBook', backref='reader', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(70))
    book_author = db.Column(db.String(100))
    book_date_publ = db.Column(db.String(5))
    book_status = db.Column(db.Boolean(), default=True)
    def __repr__(self):
        return '<Book {}, {}, {}>'.format(self.book_name, self.book_author, self.book_date_publ, self.book_status)

class ExtraditionBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    book_id = db.Column(db.Integer)
    book_name = db.Column(db.String(70))
    book_author = db.Column(db.String(100))
    book_date_publ = db.Column(db.String(5))
    exrt_date = db.Column(db.DateTime)
    arrear = db.Column(db.String(20), default=None)
    reader_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self):
        return '<ExtraditionBook {}, {}, {}, {}>'.format(self.reader_id, self.book_name, self.book_author, self.book_date_publ)

