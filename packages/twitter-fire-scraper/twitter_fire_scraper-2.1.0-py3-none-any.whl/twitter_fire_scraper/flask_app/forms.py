from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FieldList, FormField, SubmitField, PasswordField, TextField
from wtforms.validators import DataRequired, NumberRange, InputRequired, Email, Length


class ScrapeSingleTermTestForm(FlaskForm):
    """A control that lets you only gather a single search term and a single amount"""
    term = StringField('term', validators=[DataRequired()])
    amount = IntegerField('amount', validators=[NumberRange(1, 1000)])


class SingleTermForm(FlaskForm):
    """A control for a single search term with an amount."""
    term = StringField('term', validators=[DataRequired()])
    amount = IntegerField('amount', validators=[NumberRange(1, 1000)])


class RegistrationForm(FlaskForm):
    """ A control to register a new user in the website."""
    email = StringField('email', validators=[DataRequired(), Email(message="Invalid email.")])
    password = PasswordField(
        validators=[DataRequired(),
                    Length(min=8, message="Password must be at least 8 characters long."), ])
    submit = SubmitField(label="submit")


class TermsForm(FlaskForm):
    """A control which can hold multiple SingleTermForm controls."""
    terms = FieldList(FormField(SingleTermForm), min_entries=1, max_entries=10)
    submit = SubmitField(label="submit")


class AddForm(FlaskForm):
    x = IntegerField('1')
    y = IntegerField('2')
    submit = SubmitField(label='submit')


class SubDirForm(FlaskForm):
    subDirName = TextField(validators=[DataRequired()])


class SubDirsForm(FlaskForm):
    subDirList = FieldList(FormField(SubDirForm), min_entries=0)
    submit = SubmitField(label='Print')
    submit = SubmitField(label='submit')
