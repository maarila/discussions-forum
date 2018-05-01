from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, DateField, validators


class SearchForm(FlaskForm):
    search_phrase = StringField("Search", [validators.Length(min=2)])
    searching_for = RadioField("Search", choices=[
        ("topic", "topic"), ("author", "messages by")], default="topic")

    class Meta:
        csrf = False


class SearchDateForm(FlaskForm):
    date = DateField("Date")

    class Meta:
        csrf = False
