from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, SelectField, BooleanField, FileField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    price = IntegerField('Цена', default=0)
    phone = StringField('Номер телефона')
    photo = FileField('photo')
    currency = SelectField('Валюта',
                           choices=[(0, "₽"), (1, "$"), (2, "€"), (3, "₾"), (4, "₴"), (5, "₸"), (6, "Br"), (7, "₼"), ],
                           default=0)
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Описание", validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    destination = SelectField('Назначение', validators=[DataRequired()], choices=[(0, 'Поиск хозяев'), (1, "Продажа"),
                                                                                  (2, "Пристройство"),
                                                                                  (3, "Поиск питомца")], default=2)
    delivery = BooleanField('Доставка')
    submit = SubmitField('Опубликовать')
