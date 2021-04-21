from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    nickname = StringField('Никнейм', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    nickname = StringField('Никнейм', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField()