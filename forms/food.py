from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class FoodForm(FlaskForm):
    title = StringField('Purchase', validators=[DataRequired()])
    id = 0
    submit = SubmitField('Добавить в корзину')