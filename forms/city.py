from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, SearchField
from wtforms.validators import DataRequired


class CityForm(FlaskForm):
    search = SearchField('data', validators=[DataRequired()])
    city = SelectField('Город',
                           choices=[])
    submit = SubmitField('Сохранить')