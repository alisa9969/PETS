from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email


class RegisterForm(FlaskForm):
    email = EmailField('E-mail', validators=[Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    about = TextAreaField("Добавьте описание")
    submit = SubmitField('Зарегистрироваться')
