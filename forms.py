""" html form for user input """

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Optional

# create a class to take in user input
class AddAUserForm(FlaskForm):
    firstname = StringField("First Name", validators=[DataRequired()])
    lastname = StringField("Last Name", validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
    # image_url = StringField('(Optional) Image URL')


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


# Needs a form to update/edit a profile 
class UpdateUserProfileForm(FlaskForm):
    """"Profile update form """

    firstname = StringField("firstname", validators=[DataRequired()])
    lastname = StringField("lastname", validators=[DataRequired()])
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators = [Length(min = 6)]) 

    # password = PasswordField("password", render_kw={'readonly': True}, validators = [Length(min = 6)]) 
