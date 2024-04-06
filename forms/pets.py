from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, BooleanField
from wtforms.validators import DataRequired


class PetForm(FlaskForm):
    breed = StringField('Порода', validators=[DataRequired()])
    color = SelectField('Цвет', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired()])
    documents = BooleanField('Документы', validators=[DataRequired()])
    vaccin = BooleanField('Прививки', validators=[DataRequired()])
    steril = BooleanField('Стерилиация', validators=[DataRequired()])
    category = SelectField('Категория', validators=[DataRequired()])