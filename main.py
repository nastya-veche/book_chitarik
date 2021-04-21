from flask import Flask, render_template, redirect, request
from forms.user_form import LoginForm, RegisterForm
from forms.comment_form import CommentForm
from data import db_session, users_api, books_api, comments_api, genres_api
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.db_session import create_session, global_init
from data.users import User
from data.books import Book
from data.comments import Comment
from data.genres import Genre
from requests import get, post, delete, put
from werkzeug.security import generate_password_hash
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init("db/book_store.db")
app.register_blueprint(users_api.blueprint)
app.register_blueprint(books_api.blueprint)
app.register_blueprint(comments_api.blueprint)
app.register_blueprint(genres_api.blueprint)


@login_manager.user_loader
def load_user(user_id):
    db_sess = create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def main_window():
    db_sess = db_session.create_session()
    genres = db_sess.query(Genre).all()
    books = db_sess.query(Book).all()
    os.chdir('static/img/news')
    advertisement = os.listdir()
    os.chdir('..')
    os.chdir('..')
    os.chdir('..')
    return render_template('main.html', genres_list=genres, advertisement=advertisement, books_list=books,
                           title='Книги', num=5, name='Читарик')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = create_session()
        if db_sess.query(User).filter(User.nickname == form.nickname.data).first():
            return render_template('register.html', form=form, message="Такой пользователь уже есть", title="Форма регистрации")
        user = User(
            nickname=form.nickname.data,
            books=''
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        user = db_sess.query(User).filter(User.nickname == form.nickname.data).first()
        login_user(user)
        return redirect('/')
    return render_template('register.html', form=form, title="Форма регистрации", num=0)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = create_session()
        user = db_sess.query(User).filter(User.nickname == form.nickname.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/")
        return render_template('register.html',
                               message="Неправильный логин или пароль",
                               form=form, title='Авторизация')
    return render_template('register.html', title='Авторизация', form=form, num=0)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/books/<int:genre_id>')
def books_window(genre_id):
    db_sess = create_session()
    genres = db_sess.query(Genre).all()
    books = db_sess.query(Book).filter(Book.genre_id == genre_id).all()
    os.chdir('static/img/news')
    advertisement = os.listdir()
    os.chdir('..')
    os.chdir('..')
    os.chdir('..')
    title_genre = db_sess.query(Genre).get(genre_id).title
    return render_template('main.html', genres_list=genres, advertisement=advertisement,
                           books_list=books, title=f'Книги в жанре {title_genre}', num=5,
                           name=db_sess.query(Genre).filter(Genre.id == genre_id).first().title)


@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
def book_window(book_id):
    db_sess = db_session.create_session()
    genres = db_sess.query(Genre).all()
    book = db_sess.query(Book).get(book_id)
    os.chdir('static/img/news')
    advertisement = os.listdir()
    os.chdir('..')
    os.chdir('..')
    os.chdir('..')
    comments = []
    db_sess = create_session()
    for comment in db_sess.query(Comment).all():
        if str(comment.id) in book.reviews.split():
            comments.append(comment)
    title_genre = db_sess.query(Genre).get(book.genre_id).title
    form = CommentForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            db_sess = create_session()
            comment = Comment()
            comment.subject = form.subject.data
            comment.text = form.text.data
            comment.like = 0
            comment.dislike = 0
            comment.user = current_user
            db_sess.merge(comment)
            db_sess.commit()
            comment = db_sess.query(Comment).filter(Comment.user_id == current_user.id,
                                                    Comment.subject == form.subject.data).all()[-1]
            book = db_sess.query(Book).get(book_id)
            book.reviews += ' ' + str(comment.id)
            db_sess.commit()
            return redirect(f'/book/{book_id}')
        else:
            return redirect(f'/login')
    return render_template('book.html', genres_list=genres, advertisement=advertisement, book=book,
                           comments=comments, form=form, num=3, name=book.title, title_genre=title_genre)


@app.route('/like/<int:comment_id>/<int:book_id>')
def add_like(comment_id, book_id):
    db_sess = create_session()
    comment = db_sess.query(Comment).get(comment_id)
    comment.like += 1
    db_sess.commit()
    return redirect(f'/book/{book_id}')


@app.route('/dislike/<int:comment_id>/<int:book_id>')
def add_dislike(comment_id, book_id):
    db_sess = create_session()
    comment = db_sess.query(Comment).get(comment_id)
    comment.dislike += 1
    db_sess.commit()
    return redirect(f'/book/{book_id}')


@app.route('/find/<text>')
def find(text):
    db_sess = create_session()
    genres = db_sess.query(Genre).all()
    books = []
    for item in db_sess.query(Book).all():
        if text.lower() in item.title.lower():
            books.append(item)
    os.chdir('static/img/news')
    advertisement = os.listdir()
    os.chdir('..')
    os.chdir('..')
    os.chdir('..')
    return render_template('main.html', genres_list=genres, advertisement=advertisement, books_list=books,
                           title='Книги', num=5, name='Поиск книги')


@app.route('/conservation/<int:book_id>')
def conservation(book_id):
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(current_user.id)
        user.books += ' ' + str(book_id)
        db_sess.commit()
        return redirect(f'/book/{book_id}')
    return redirect(f'/login')


@app.route('/profile')
def profile():
    db_sess = db_session.create_session()
    genres = db_sess.query(Genre).all()
    print(db_sess.query(User).get(current_user.id).books)
    list_books = [int(i) for i in db_sess.query(User).get(current_user.id).books.split()]
    books = db_sess.query(Book).filter(Book.id.in_(list_books)).all()
    os.chdir('static/img/news')
    advertisement = os.listdir()
    os.chdir('..')
    os.chdir('..')
    os.chdir('..')
    return render_template('main.html', genres_list=genres, advertisement=advertisement,
                           books_list=books, title=f'Сохраненные книги', num=5, name='Профиль')


#if __name__ == '__main__':
    #app.run(port=8080, host='127.0.0.1')
    #app.run()


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)