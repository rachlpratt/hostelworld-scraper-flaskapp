from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField


destinations = ['Paris, France', 'Tokyo, Japan', 'Milan, Italy']


class SelectDestinationForm(FlaskForm):
    destination = SelectField(label='Destination', choices=destinations)
    submit = SubmitField('Select')
