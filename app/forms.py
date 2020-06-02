from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User, Book, ExtraditionBook


class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField('Повтрите пароль', validators=[DataRequired(), EqualTo('password')])
    fio = StringField('ФИО', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    submit = SubmitField('Вперёд!')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста, используйте другой логин.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста, используйте другой email-адрес.')


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня?')
    submit = SubmitField('Войти!')

class BookForm(FlaskForm):
    book_name = StringField('Название', validators=[DataRequired()])
    book_author = StringField('Автор', validators=[DataRequired()])
    book_date_publ = StringField('Год издания', validators=[DataRequired()])
    submit = SubmitField('Добавить!')


class ExtraditionBookForm(FlaskForm):
    book = SelectField('Книга', coerce=int)
    reader = SelectField('Читатель', coerce=int)
    submit = SubmitField('Выдать!')

class PlsForm(FlaskForm):
    submit = SubmitField('Запросить!')