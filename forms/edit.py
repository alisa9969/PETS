from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, Length


class EditForm(FlaskForm):
    email = EmailField('E-mail', validators=[Email(), Length(max=40)])
    name = StringField('Имя пользователя', validators=[DataRequired(), Length(max=18)])
    about = TextAreaField("Добавьте описание", validators=[Length(max=150)])
    submit = SubmitField('Сохранить')
