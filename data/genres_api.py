from . import db_session
from .genres import Genre
import flask
from flask import jsonify, request


blueprint = flask.Blueprint(
    'genres_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/get_genres')
def get_genres():
    db_sess = db_session.create_session()
    genres = db_sess.query(Genre).all()
    return genres


@blueprint.route('/get_one_genre/<int:genre_id>', methods=['GET'])
def get_one_genre(genre_id):
    db_sess = db_session.create_session()
    genre = db_sess.query(Genre).get(genre_id)
    return genre


@blueprint.route('/create_genre', methods=['POST'])
def create_genre():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['title']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    genre = Genre(
        title=request.json['title']
    )
    db_sess.add(genre)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/delete_genre/<int:genre_id>', methods=['DELETE'])
def delete_genre(genre_id):
    db_sess = db_session.create_session()
    genre = db_sess.query(Genre).get(genre_id)
    if not genre:
        return jsonify({'error': 'Not found'})
    db_sess.delete(genre)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/change_genre/<int:genre_id>', methods=['PUT'])
def change_genre(genre_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['title']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    genre = db_sess.query(Genre).get(genre_id)
    if not genre:
        return jsonify({'error': 'Not found'})
    genre.title = request.json['title']
    db_sess.commit()
    return jsonify({'success': 'OK'})