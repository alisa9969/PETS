from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, BooleanField, StringField
from wtforms.validators import DataRequired


class PetForm(FlaskForm):
    breed = StringField('Порода', validators=[DataRequired()])
    color = SelectField('Цвет',
                        choices=[(0, "Белый"), (1, "Черный"), (2, "Серый"),
                                 (3, "Рыжий"), (4, "Золотистый"), (5, "Зеленый"),
                                 (6, "Синий"), (7, "Розовый"), (8, "Коричневый"), (9, "Фиолетовый"), (10, "Красный"),
                                 (11, "Бежевый"), (12, "Разноцветный")], default=0)
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
