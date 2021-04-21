from . import db_session
from .users import User
import flask
from flask import jsonify, request
from werkzeug.security import generate_password_hash


blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/get_users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return users


@blueprint.route('/get_one_user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    return user


@blueprint.route('/create_user', methods=['POST'])
def create_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['nickname', 'hashed_password']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    user = User(
        nickname=request.json['nickname'],
        hashed_password=generate_password_hash(request.json['hashed_password']),
        books=''
    )
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/change_user/<int:user_id>', methods=['PUT'])
def change_user(user_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['nickname', 'hashed_password', 'books']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    user.nickname = request.json['nickname']
    user.hashed_password = generate_password_hash(request.json['hashed_password'])
    user.books = request.json['books']
    db_sess.commit()
    return jsonify({'success': 'OK'})