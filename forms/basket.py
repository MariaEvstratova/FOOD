from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField, IntegerField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import NumberInput


class BasketForm(FlaskForm):
    submit = SubmitField('Удалить')