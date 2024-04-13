from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = EmailField('E-mail', validators=[Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
