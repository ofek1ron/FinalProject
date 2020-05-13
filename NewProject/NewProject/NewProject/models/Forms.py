### ----------------------------------------------------------- ###
### ----- includes all software packages that are needed ------ ###
### ----------------------------------------------------------- ###
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import Form, BooleanField, PasswordField , HiddenField , DateTimeField , IntegerField , DecimalField , FloatField , RadioField
from wtforms import Form, SelectMultipleField , BooleanField
from wtforms import TextField, TextAreaField, SelectField
from wtforms import validators, ValidationError
from wtforms.fields.html5 import DateField

from wtforms.validators import DataRequired
from wtforms.validators import InputRequired


##   This form is where the user can set different parameters
##   that will be used to do the data analysis (using Pandas etc.)
class NBAForm(FlaskForm):
    player_a = SelectField('NBA Player 1:' , validators = [DataRequired]) # Makes a new input field on the query page with a predetermined selection.
    player_b = SelectField('NBA Player 2:' , validators = [DataRequired])
    catagory = SelectField('Comparison Category' , validators = [DataRequired])
    kind = SelectField('Chart Kind' , validators = [DataRequired] , choices=[('Line', 'Line'), ('Bar', 'Bar')]) # The chart kind options
    subnmit = SubmitField('Display') # Sumbit button


##   This class has the fields that the user can set, to have the query parameters for analysing the data.
##   This form is where the user can set different parameters, that will be used to do data analysis.
## You can see three fields:
##   The 'submit' button - the button the user will press to have the 
##   form be "posted" (sent to the server for process).
class ExpandForm(FlaskForm):
    submit1 = SubmitField('Expand')
    name="Expand" 
    value="Expand"

class CollapseForm(FlaskForm):
    submit2 = SubmitField('Collapse')
    name="Collapse" 
    value="Collapse"
