from flask import render_template, url_for, flash, redirect, request, abort
from app import app, db
from app.forms import RegistrationForm, LoginForm, BookForm, ExtraditionBookForm, PlsForm
from app.models import User, Post, Book, ExtraditionBook
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, fio=form.fio.data, address=form.address.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Успешная регистрация!', "success")
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')

@app.route('/books', methods=['GET', 'POST'])
@login_required
def add_book():
    # if current_user.role != 'admin':
    #     abort(403)
    form = BookForm()
    if form.validate_on_submit():
        book = Book(book_name = form.book_name.data, book_author = form.book_author.data, book_date_publ = form.book_date_publ.data)
        db.session.add(book)
        db.session.commit()
        flash('Книга в базе:)', 'success')
        return redirect(url_for('add_book'))
    return render_template('books.html', title='База книг', form=form, book_get=Book.query.all())

@app.route('/extradition_book', methods=['GET', 'POST'])
@login_required
def extradition_book():
    # lead = ExtraditionBook.query.get_or_404(1)
    # db.session.delete(lead)
    # db.session.commit()
    form = ExtraditionBookForm()
    form.book.choices = [(int(bk.id), str(bk.book_name)) for bk in Book.query.all() if bk.book_status != False]
    form.reader.choices = [(int(rd.id), str(rd.fio)) for rd in User.query.all() if rd.role != 'admin']
    if form.validate_on_submit():
        ch_id_book = request.form.get('book')
        eb = ExtraditionBook(book_id = ch_id_book, book_name = Book.query.filter_by(id=ch_id_book).first().book_name, book_author = Book.query.filter_by(id=ch_id_book).first().book_author, book_date_publ = Book.query.filter_by(id=ch_id_book).first().book_date_publ, reader_id = Book.query.filter_by(id=request.form.get('reader')).first().id, exrt_date = datetime.strptime(request.form.get('ex_date'), "%Y-%m-%d").date())
        Book.query.filter_by(id=ch_id_book).first().book_status = False
        db.session.add(eb)
        db.session.commit()
        flash('Выдача произведена!', 'success')
        return redirect(url_for('extradition_book'))
    elif form.errors:
        print(form.errors)
    return render_template('extradition_book.html', title='Выдача книг', form=form, eb_get=ExtraditionBook.query.all(), users=User.query.all())

@app.route("/arrears")
@login_required
def arrears():
    return render_template('arrears.html', title='Долги читателя')

@app.route("/adm_arrears")
@login_required
def adm_arrears():
    if current_user.role != 'admin':
        abort(403)
    return render_template('adm_arrears.html', title='Запросы на продление', ex_books=ExtraditionBook.query.all(), users=User.query.all())

@app.route("/extradition_book/<int:eb_id><int:book_id>/del", methods=['GET', 'POST'])
@login_required
def delete_eb(eb_id, book_id):
    if current_user.role != 'admin':
        abort(403)
    eb = ExtraditionBook.query.get_or_404(eb_id)
    Book.query.filter_by(id=book_id).first().book_status = True
    db.session.delete(eb)
    db.session.commit()
    flash('Должник удалён!', 'success')
    return redirect(url_for('extradition_book'))

@app.route("/arr_please/<int:arr_id>", methods=['GET', 'POST'])
@login_required
def arr_please(arr_id):
    eb = ExtraditionBook.query.get_or_404(arr_id)
    if eb.reader != current_user:
        abort(403)
    form = PlsForm()
    if form.validate_on_submit():
        if eb.arrear == 'Отклонено' or eb.arrear == 'Одобрено':
            flash('Запрос можно отправлять только один раз!!!', 'warning')
            return redirect(url_for('arrears'))
        eb.arrear = request.form.get('arr_date')
        db.session.commit()
        flash('Запрос отправлен!', 'success')
        return redirect(url_for('arrears'))
    return render_template('arr_please.html', title='Запросить продление сроков', form=form)

@app.route("/adm_arrears/<int:arr_id>/ok", methods=['GET', 'POST'])
@login_required
def arr_ok(arr_id):
    if current_user.role != 'admin':
        abort(403)
    eb = ExtraditionBook.query.get_or_404(arr_id)
    eb.exrt_date = datetime.strptime(eb.arrear, "%Y-%m-%d").date()
    eb.arrear = 'Одобрено'
    db.session.commit()
    flash('Срок продлён!', 'success')
    return redirect(url_for('adm_arrears'))

@app.route("/adm_arrears/<int:arr_id>/no", methods=['GET', 'POST'])
@login_required
def arr_no(arr_id):
    if current_user.role != 'admin':
        abort(403)
    eb = ExtraditionBook.query.get_or_404(arr_id)
    eb.arrear = 'Отклонено'
    db.session.commit()
    flash('Запрос отклонён!', 'success')
    return redirect(url_for('adm_arrears'))