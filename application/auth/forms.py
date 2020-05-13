from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators

class LoginForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=1)])
    password = PasswordField("Password", [validators.Length(min=1)])

    class Meta:
        csrf = False

class RegisterForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=2, max=60)])
    username = StringField("Username", [validators.Length(min=1, max=60)])
    password = PasswordField("Password", [validators.Length(min=4, max=30)])
    
    class Meta:
        csrf = False

