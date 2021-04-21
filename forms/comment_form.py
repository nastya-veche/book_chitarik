from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField, TextAreaField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):
    subject = StringField('Тема', validators=[DataRequired()])
    text = TextAreaField('Отзыв', validators=[DataRequired()])
    #text = StringField('Отзыв', validators=[DataRequired()])
    submit = SubmitField('Оставить отзыв')
