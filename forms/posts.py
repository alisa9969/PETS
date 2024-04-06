from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, SelectField, BooleanField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    price = IntegerField('Цена', validators=[DataRequired()])
    phone = StringField('Номер телефона', validators=[DataRequired()])
    currency = SelectField('Валюта', validators=[DataRequired()],
                           choices=[(0, "₽"), (1, "$"), (2, "€"), (3, "₾"), (4, "₴"), (5, "₸"), (6, "Br"), (7, "₼"), ])
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Описание")
    address = StringField('Адрес', validators=[DataRequired()])
    destination = SelectField('Назначение', validators=[DataRequired()], choices=[(0, 'Поиск хозяев'), (1, "Продажа"),
                                                                                  (2, "Пристроство"),
                                                                                  (3, "Поиск питомца")])
    delivery = BooleanField('Доставка', validators=[DataRequired()])
    submit = SubmitField('Опубликовать')
