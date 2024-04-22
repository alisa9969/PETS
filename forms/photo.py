from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField


class PhotoForm(FlaskForm):
    photo = FileField('photo', default="")
    submit = SubmitField('Загрузить')
