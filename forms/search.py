from flask_wtf import FlaskForm
from wtforms import SearchField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    search = SearchField('data', validators=[DataRequired()])
    submit = SubmitField('search')
