from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, SelectField, BooleanField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    price = IntegerField('Цена', validators=[DataRequired()])
    phone = StringField('Номер телефона', validators=[DataRequired()])
    currency = SelectField('Валюта', validators=[DataRequired()])
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Описание")
    address = StringField('Адрес', validators=[DataRequired()])
    destination = SelectField('Назначение', validators=[DataRequired()])
    delivery = BooleanField('Доставка', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')
