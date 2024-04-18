from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, SelectField, BooleanField, FileField, TelField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    price = IntegerField('Цена', default=0)
    phone = TelField('Номер телефона', validators=[Length(max=19)])
    photo = FileField('photo', default="")
    currency = SelectField('Валюта',
                           choices=["₽", "$", "€", "₾", "₴", "₸", "Br", "₼"],
                           default="₽")
    title = StringField('Заголовок', validators=[DataRequired(), Length(max=18)])
    content = TextAreaField("Описание", validators=[DataRequired(), Length(max=400)])
    address = StringField('Адрес', validators=[DataRequired(), Length(max=100)])
    destination = SelectField('Назначение', validators=[DataRequired()], choices=['Поиск хозяев',
                                                                                  "Пристройство",
                                                                                  "Поиск питомца"],
                              default="Пристройство")
    delivery = BooleanField('Доставка')
    breed = StringField('Порода', validators=[DataRequired(), Length(max=50)])
    color = SelectField('Цвет',
                        choices=["Белый", "Черный", "Серый",
                                 "Рыжий", "Золотистый", "Зеленый",
                                 "Синий", "Розовый", "Коричневый", "Фиолетовый", "Красный",
                                 "Бежевый", "Разноцветный"], default="Белый")
    age = IntegerField('Возраст', default=0)
    documents = BooleanField('Документы')
    vaccin = BooleanField('Прививки')
    steril = BooleanField('Стерилизация')
    category = SelectField('Категория',
                           choices=[('cats', "Кошки"), ('dogs', "Собаки"), ('waterfowl', "Аквариумные"),
                                    ('rodents', "Грызуны"), ('reptiles', "Рептилии"),
                                    ('insects', "Насекомые"), ('arachnids', "Паукообразные"),
                                    ('exotic', "Экзотические животные"),
                                    ('shellfish', "Моллюски"), ('birds', "Птицы"), ('farm', "Ферма")], default=0)
    submit = SubmitField('Опубликовать')
