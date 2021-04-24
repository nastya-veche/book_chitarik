from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField, TextAreaField, IntegerField
from wtforms.validators import DataRequired


class BookForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    author = StringField('Автор', validators=[DataRequired()])
    age_limit = IntegerField('Возрастное ограничение', validators=[DataRequired()])
    annotation = TextAreaField('Отзыв', validators=[DataRequired()])
    submit = SubmitField('Добавить книгу')