""" flask wtf(what the form)for user input. """

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Optional


class AddAUserForm(FlaskForm):
    """ create a class to take in user input for signing up the user. """

    firstname = StringField("First Name", validators=[DataRequired()])
    lastname = StringField("Last Name", validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class LoginForm(FlaskForm):
    """ User login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class UpdateUserProfileForm(FlaskForm):
    """" User profile update form. """

    firstname = StringField("firstname", validators=[DataRequired()])
    lastname = StringField("lastname", validators=[DataRequired()])
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators = [Length(min = 6)]) 

