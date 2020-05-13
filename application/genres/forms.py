from flask_wtf import FlaskForm
from wtforms import StringField, validators

class GenreForm(FlaskForm):
    name = StringField("Genre name", [validators.Length(min=1, max=50)])

    class Meta:
        csrf = False
