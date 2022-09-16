""" flask wtf(what the form)for user input. """

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Length, InputRequired


class AddAUserForm(FlaskForm):
    """ create a class to take in user input for signing up the user. """

    firstname = StringField("First Name", validators=[InputRequired(message="First name should contain only letters and cannot be blank.")])
    lastname = StringField("Last Name", validators=[InputRequired(message="Last name should contain only letters and cannot be blank.")])
    username = StringField('Username', validators=[InputRequired(message="Username can have only letters and numbers.")])
    password = PasswordField('Password', validators=[Length(min=6, message="Password must be at least 6 characters."), 
                                        InputRequired(message="Password must be at least 6 characters.")])


class LoginForm(FlaskForm):
    """ User login form."""

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[Length(min=6), InputRequired()])


class UpdateUserProfileForm(FlaskForm):
    """" User profile update form. """

    firstname = StringField("First Name", validators=[InputRequired(message="First name should contain only letters and cannot be blank.")])
    lastname = StringField("Last Name", validators=[InputRequired(message="Last name should contain only letters and cannot be blank.")])
    username = StringField("Username", validators=[InputRequired(message="Username can have only letters and numbers.")])
    password = PasswordField("Password", validators = [Length(min = 6), InputRequired(message="Password must be at least 6 characters.")]) 

