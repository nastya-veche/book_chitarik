from . import db_session
from .books import Book
import flask
from flask import jsonify, request


blueprint = flask.Blueprint(
    'books_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/get_books')
def get_books():
    db_sess = db_session.create_session()
    books = db_sess.query(Book).all()
    return books


@blueprint.route('/get_one_book/<int:book_id>', methods=['GET'])
def get_one_book(book_id):
    db_sess = db_session.create_session()
    book = db_sess.query(Book).get(book_id)
    return book


@blueprint.route('/create_book', methods=['POST'])
def create_book():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['title', 'author', 'age_limit', 'annotation',
                  'cover_art', 'genre_id', 'reviews']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    book = Book(
        title=request.json['title'],
        author=request.json['author'],
        age_limit=request.json['age_limit'],
        annotation=request.json['annotation'],
        cover_art=request.json['cover_art'],
        genre_id=request.json['genre_id'],
        reviews=request.json['reviews']
    )
    db_sess.add(book)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/delete_book/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    db_sess = db_session.create_session()
    book = db_sess.query(Book).get(book_id)
    if not book:
        return jsonify({'error': 'Not found'})
    db_sess.delete(book)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/change_book/<int:book_id>', methods=['PUT'])
def change_book(book_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['title', 'author', 'age_limit', 'annotation',
                  'cover_art', 'genre_id', 'reviews']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    book = db_sess.query(Book).get(book_id)
    if not book:
        return jsonify({'error': 'Not found'})
    book.title = request.json['title']
    book.author = request.json['author']
    book.age_limit = request.json['age_limit']
    book.annotation = request.json['annotation']
    book.cover_art = request.json['cover_art']
    book.genre_id = request.json['genre_id']
    book.reviews = request.json['reviews']
    db_sess.commit()
    return jsonify({'success': 'OK'})