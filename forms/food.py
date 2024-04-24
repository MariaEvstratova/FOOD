from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField, IntegerField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import NumberInput


class FoodForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    number = IntegerField('Номер телефона', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    submit = SubmitField('Купить')