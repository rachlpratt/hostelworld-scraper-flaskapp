from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField


class SelectDestinationForm(FlaskForm):
    destination = SelectField(label='Destination')
    submit = SubmitField('Select')
