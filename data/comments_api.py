from . import db_session
from .comments import Comment
import flask
from flask import jsonify, request


blueprint = flask.Blueprint(
    'comments_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/get_comments')
def get_comments():
    db_sess = db_session.create_session()
    comments = db_sess.query(Comment).all()
    return comments


@blueprint.route('/get_one_comment/<int:comment_id>', methods=['GET'])
def get_one_comment(comment_id):
    db_sess = db_session.create_session()
    comment = db_sess.query(Comment).get(comment_id)
    return comment


@blueprint.route('/create_comment', methods=['POST'])
def create_comment():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['text', 'subject', 'like', 'dislike', 'user_id']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    comment = Comment(
        text=request.json['text'],
        user_id=request.json['user_id'],
        subject=request.json['subject'],
        like=request.json['like'],
        dislike=request.json['dislike']
    )
    db_sess.add(comment)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/delete_comment/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    db_sess = db_session.create_session()
    comment = db_sess.query(Comment).get(comment_id)
    if not comment:
        return jsonify({'error': 'Not found'})
    db_sess.delete(comment)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/change_comment/<int:comment_id>', methods=['PUT'])
def change_comment(comment_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['text', 'subject', 'like', 'dislike', 'user_id']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    comment = db_sess.query(Comment).get(comment_id)
    if not comment:
        return jsonify({'error': 'Not found'})
    comment.text = request.json['text']
    comment.subject = request.json['subject']
    comment.like = request.json['like']
    comment.dislike = request.json['dislike']
    comment.user_id = request.json['user_id']
    db_sess.commit()
    return jsonify({'success': 'OK'})