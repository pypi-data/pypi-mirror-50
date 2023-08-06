from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FieldList, FormField, SubmitField, PasswordField, TextField, BooleanField
from wtforms.validators import DataRequired, NumberRange, InputRequired, Email, Length


class ScrapeSingleTermTestForm(FlaskForm):
    """A control that lets you only gather a single search term and a single amount"""
    term = StringField('term', validators=[DataRequired()])
    amount = IntegerField('amount', validators=[NumberRange(1, 1000)])
    submit = SubmitField(label='gather')

    # TODO This is a temporary field until we allow users to edit and remove tweets before saving them via JavaScript.
    # TODO This is also useful for adding Tweets for testing the Database page.
    saveToDatabase = BooleanField(label='save to database?')


class SingleTermForm(FlaskForm):
    """A control for a single search term with an amount."""
    term = StringField('term', validators=[DataRequired()])
    amount = IntegerField('amount', validators=[NumberRange(1, 1000)])
    submit = SubmitField(label='submit')


class TermsForm(FlaskForm):
    """A control which can hold multiple SingleTermForm controls."""
    terms = FieldList(FormField(SingleTermForm), min_entries=1)
    # submit = SubmitField(label="Submit")


class RegistrationForm(FlaskForm):
    """ A control to register a new user in the website."""
    email = StringField('email', validators=[DataRequired(), Email(message="Invalid email.")])
    password = PasswordField(
        validators=[DataRequired(),
                    Length(min=8, message="Password must be at least 8 characters long."), ])
    submit = SubmitField(label="register")


class LoginForm(RegistrationForm):
    """ A control to log into the website."""
    submit = SubmitField(label='login')


class AddForm(FlaskForm):
    x = IntegerField('1')
    y = IntegerField('2')
    submit = SubmitField(label='submit')
