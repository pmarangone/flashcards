from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, EqualTo

class SignUpForm(FlaskForm):
    username = StringField("Username", validators = [InputRequired()])
    password = PasswordField('Password', validators = [InputRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators = [InputRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField("Username", validators = [InputRequired()])
    password = PasswordField('Password', validators = [InputRequired()])
    submit = SubmitField()
    
class CreateCard(FlaskForm):
    deck_name = StringField("Deck", validators = [InputRequired()])
    front = StringField("Front", validators = [InputRequired()])
    back = StringField("Back", validators = [InputRequired()])
    submit = SubmitField("Create card")

class CreateDeck(FlaskForm):
    name = StringField("Name", validators = [InputRequired()])
    summary = StringField("Summary", validators = [InputRequired()])
    submit = SubmitField("Create deck")