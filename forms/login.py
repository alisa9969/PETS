from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    email = EmailField('E-mail', validators=[Email(), Length(max=40)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(max=20)])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
