from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class MeteostationForm(FlaskForm):
    meteostation = SelectField('Meteostation', validators=[DataRequired()], coerce=int)
    part_name = StringField('Write part of name')
    submit = SubmitField('Filter')
