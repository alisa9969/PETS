from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, Length


class RegisterForm(FlaskForm):
    email = EmailField('E-mail', validators=[Email(), Length(max=40)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6, max=20)])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired(), Length(min=6, max=20)])
    name = StringField('Имя пользователя', validators=[DataRequired(), Length(max=18)])
    about = TextAreaField("Добавьте описание", validators=[Length(max=150)])
    submit = SubmitField('Зарегистрироваться')
