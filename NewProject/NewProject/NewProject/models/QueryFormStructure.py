### ----------------------------------------------------------- ###
### ----- includes all software packages that are needed ------ ###
### ----------------------------------------------------------- ###
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import Form, BooleanField, PasswordField
from wtforms import TextField, TextAreaField, SelectField, DateField
from wtforms import validators, ValidationError
from wtforms.validators import DataRequired
from wtforms.validators import InputRequired

## This class has the fields that are part of the Login form.
##   This form will get from the user a 'username' and a 'password' and send to the server
##   to check if this user is authorised to ablt continue to the query.
##  You can see three fields:
##   the 'username' field - will be used to get the username.
##   the 'password' field - will be used to get the password.
##   the 'submit' button - the button the user will press to have the 
##   form be "posted" (sent to the server for process).
class LoginFormStructure(FlaskForm):
    username   = StringField('User name:  ' , validators = [DataRequired()])
    password   = PasswordField('Pass word:  ' , validators = [DataRequired()])
    submit = SubmitField('Submit')



## This class has the fields of a registration form.
##   This form is where the user can register himself. It will have the information
##   we want to save on a user (general information) and the username.
## You can see three fields:
##   the 'FirstName' field - will be used to get the first name of the user.
##   the 'LastName' field - will be used to get the last name of the user.
##   the 'PhoneNum' field - will be used to get the phone number of the user.
##   the 'EmailAddr' field - will be used to get the E-Mail of the user.
##   the 'username' field - will be used to get the username.
##   the 'password' field - will be used to get the password.
##   the 'submit' button - the button the user will press to have the 
##   form be "posted" (sent to the server for process).
class UserRegistrationFormStructure(FlaskForm):
    FirstName  = StringField('First name:  ' , validators = [DataRequired()])
    LastName   = StringField('Last name:  ' , validators = [DataRequired()])
    PhoneNum   = StringField('Phone number:  ' , validators = [DataRequired()])
    EmailAddr  = StringField('E-Mail:  ' , validators = [DataRequired()])
    username   = StringField('User name:  ' , validators = [DataRequired()])
    password   = PasswordField('Pass word:  ' , validators = [DataRequired()])
    submit = SubmitField('Submit')

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