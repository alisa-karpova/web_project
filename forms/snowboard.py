from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField
from wtforms import BooleanField, SubmitField, StringField
from wtforms.validators import DataRequired, NumberRange


class SnowboardsForm(FlaskForm):
    height = IntegerField('Ваш рост', default=140, validators=[DataRequired(), NumberRange(min=140, max=205)])
    weight = IntegerField('Ваш вес', default=35, validators=[DataRequired(), NumberRange(min=35, max=100)])
    level = SelectField('Уровень катания', validators=[DataRequired()],
                        choices=[('beginner', 'Начинающий (не освоил базовую технику)'),
                                 ('experienced', 'Имею опыт катания (освоил базовую технику)'),
                                 ('pro', 'Профи')])
    style = SelectField('Стиль катания', validators=[DataRequired()],
                        choices=[('base', 'Базовая техника'),
                                 ('carving', 'Карвинг'),
                                 ('freestyle', 'Фристайл'),
                                 ('freeride', 'Фрирайд'),
                                 ('carving_freestyle', 'Карвинг и фристайл'),
                                 ('carving_freeride', 'Карвинг и фрирайд')])
    high_tramps = BooleanField("Будете ли Вы делать трюки с больших трамплинов?")
    submit = SubmitField('Отправить')