from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired


class FilterForm(FlaskForm):
    price1 = IntegerField('Цена min', default=0)
    price2 = IntegerField('Цена max', default=1000000)
    destination = SelectMultipleField('Назначение', validators=[DataRequired()], choices=['Все', 'Поиск хозяев',
                                                                                  "Пристройство",
                                                                                  "Поиск питомца"],
                              default='Все')
    delivery = BooleanField('Доставка')
    color = SelectMultipleField('Цвет',
                        choices=['Все', "Белый", "Черный", "Серый",
                                 "Рыжий", "Золотистый", "Зеленый",
                                 "Синий", "Розовый", "Коричневый", "Фиолетовый", "Красный",
                                 "Бежевый", "Разноцветный"], default='Все')
    age = IntegerField('Возраст min', default=0)
    age2 = IntegerField('Возраст max', default=0)
    documents = BooleanField('Документы')
    vaccin = BooleanField('Прививки')
    steril = BooleanField('Стерилизация')
    category = SelectMultipleField('Категория',
                           choices=['Все', ('cats', "Кошки"), ('dogs', "Собаки"), ('waterfowl', "Аквариумные"),
                                    ('rodents', "Грызуны"), ('reptiles', "Рептилии"),
                                    ('insects', "Насекомые"), ('arachnids', "Паукообразные"),
                                    ('exotic', "Экзотические животные"),
                                    ('shellfish', "Моллюски"), ('birds', "Птицы"), ('farm', "Ферма")], default='Все')
    submit = SubmitField('Применить')
