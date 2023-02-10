from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

# destinations = [["tokyo", "japan"], ["paris", "france"], ["milan", "italy"], ["sydney", "australia"],
#                 ["new york city", "usa"], ["san francisco", "usa"], ["istanbul", "turkey"], ["athens", "greece"],
#                 ["hong kong", "hong kong"], ["taipei", "taiwan"], ["san juan", "puerto rico"],
#                 ["glasgow", "united kingdom"], ["dublin", "ireland"], ["auckland", "new zealand"]]


class SelectDestinationForm(FlaskForm):
    destination = SelectField(label='Destination')
    submit = SubmitField('Select')
