from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length
from flask_wtf import FlaskForm


class login_form(FlaskForm):
    """
    A FlaskForm class representing a login form.

    Attributes:
    -----------
    username : StringField
        A string field for the username input.
    pwd : PasswordField
        A password field for the password input.

    Methods:
    --------
    None
    """

    username = StringField(validators=[InputRequired()])
    pwd = PasswordField(validators=[InputRequired(), Length(min=8, max=72)])
