from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SelectMultipleField, validators, widgets
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField

from application.genres.models import Genre

class MultiCheckboxField(QuerySelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

def genres_query():
    return Genre.query


class ContentForm(FlaskForm):
    name = StringField("Title", [validators.Length(min=1, max=100)])
    length = IntegerField("Length (in minutes)", [validators.NumberRange(min=0, max=999999)])
    category = MultiCheckboxField("Genre(s)", query_factory=genres_query, allow_blank=True, get_label='name')
    cdn = SelectField("Content provider", choices=[("HBO", "HBO"), ("Netflix", "Netflix"), ("Amazon Prime", "Amazon Prime")])

    class Meta:
        csrf = False

